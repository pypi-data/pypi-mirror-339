__author__ = "Simon Nilsson"

import functools
import multiprocessing
import os
import platform
from copy import deepcopy
from typing import Dict, Optional, Tuple, Union

import cv2
import numpy as np

from simba.mixins.config_reader import ConfigReader
from simba.mixins.plotting_mixin import PlottingMixin
from simba.mixins.train_model_mixin import TrainModelMixin
from simba.utils.checks import (check_file_exist_and_readable, check_float,
                                check_if_keys_exist_in_dict, check_instance,
                                check_int, check_valid_boolean)
from simba.utils.data import create_color_palette
from simba.utils.enums import ConfigKey, Dtypes, Formats, TagNames, TextOptions
from simba.utils.errors import NoSpecifiedOutputError
from simba.utils.printing import SimbaTimer, log_event, stdout_success
from simba.utils.read_write import (concatenate_videos_in_folder,
                                    find_core_cnt, get_fn_ext,
                                    get_video_meta_data, read_config_entry,
                                    read_df)

CIRCLE_SCALE = 'circle_scale'
FONT_SIZE = 'font_size'
SPACE_SCALE = 'spacing_scale'
TEXT_THICKNESS = 'text_thickness'
TEXT_SETTING_KEYS = ['circle_scale', 'font_size', 'spacing_scale', 'text_thickness']
CENTER_BP_TXT = ['centroid', 'center']

def _multiprocess_sklearn_video(data: np.array,
                                video_path: str,
                                video_save_dir: str,
                                frame_save_dir: str,
                                clf_colors: list,
                                models_info: dict,
                                bp_dict: dict,
                                text_attr: dict,
                                rotate: bool,
                                print_timers: bool,
                                video_setting: bool,
                                frame_setting: bool,
                                pose_threshold: float):

    def _put_text(img: np.ndarray,
                  text: str,
                  pos: Tuple[int, int],
                  font_size: int,
                  font_thickness: Optional[int] = 2,
                  font: Optional[int] = cv2.FONT_HERSHEY_DUPLEX,
                  text_color: Optional[Tuple[int, int, int]] = (255, 255, 255),
                  text_color_bg: Optional[Tuple[int, int, int]] = (0, 0, 0),
                  text_bg_alpha: float = 0.8):

        x, y = pos
        text_size, px_buffer = cv2.getTextSize(text, font, font_size, font_thickness)
        w, h = text_size
        overlay, output = img.copy(), img.copy()
        cv2.rectangle(overlay, (x, y-h), (x + w, y + px_buffer), text_color_bg, -1)
        cv2.addWeighted(overlay, text_bg_alpha, output, 1 - text_bg_alpha, 0, output)
        cv2.putText(output, text, (x, y), font, font_size, text_color, font_thickness)
        return output

    fourcc, font = cv2.VideoWriter_fourcc(*"mp4v"), cv2.FONT_HERSHEY_DUPLEX
    video_meta_data = get_video_meta_data(video_path=video_path)
    cap = cv2.VideoCapture(video_path)
    group = data["group"].iloc[0]
    start_frm, current_frm, end_frm = (data["index"].iloc[0], data["index"].iloc[0], data["index"].iloc[-1])
    if video_setting:
        video_save_path = os.path.join(video_save_dir, f"{group}.mp4")
        video_writer = cv2.VideoWriter(video_save_path, fourcc, video_meta_data["fps"], (video_meta_data["width"], video_meta_data["height"]))
    cap.set(1, start_frm)
    while current_frm < end_frm:
        ret, img = cap.read()
        add_spacer = 2
        for animal_name, animal_data in bp_dict.items():
            animal_clr = animal_data["colors"]
            id_flag_cords = None
            for bp_no in range(len(animal_data["X_bps"])):
                bp_clr = animal_clr[bp_no]
                x_bp, y_bp, p_bp = (animal_data["X_bps"][bp_no], animal_data["Y_bps"][bp_no], animal_data["P_bps"][bp_no])
                bp_cords = data.loc[current_frm, [x_bp, y_bp, p_bp]]
                if bp_cords[p_bp] > pose_threshold:
                    cv2.circle(img, (int(bp_cords[x_bp]), int(bp_cords[y_bp])), text_attr["circle_scale"], bp_clr, -1)
                    if x_bp.lower() in CENTER_BP_TXT:
                        id_flag_cords = (int(bp_cords[x_bp]), int(bp_cords[y_bp]))

            if not id_flag_cords:
                id_flag_cords = (int(bp_cords[x_bp]), int(bp_cords[y_bp]))
            cv2.putText(img, animal_name, id_flag_cords, font, text_attr[FONT_SIZE], animal_clr[0], text_attr[TEXT_THICKNESS])
        if rotate:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        if print_timers:
            img = _put_text(img=img, text="TIMERS:", pos=(TextOptions.BORDER_BUFFER_Y.value, text_attr[SPACE_SCALE]), font_size=text_attr[FONT_SIZE], font_thickness=text_attr[TEXT_THICKNESS], font=font, text_color=(255, 255, 255))
        frame_results = {}
        for model in models_info.values():
            frame_results[model["model_name"]] = data.loc[current_frm, model["model_name"]]
            if print_timers:
                cumulative_time = round(data.loc[current_frm, model["model_name"] + "_cumsum"] / video_meta_data["fps"], 3)
                img = _put_text(img=img, text=f"{model['model_name']} {cumulative_time}s", pos=(TextOptions.BORDER_BUFFER_Y.value, text_attr[SPACE_SCALE] * add_spacer), font_size=text_attr[FONT_SIZE], font_thickness=text_attr[TEXT_THICKNESS], font=font, text_color=(255, 255, 255))
                add_spacer += 1
        img = _put_text(img=img, text="ENSEMBLE PREDICTION:", pos=(TextOptions.BORDER_BUFFER_Y.value, text_attr[SPACE_SCALE] * add_spacer), font_size=text_attr[FONT_SIZE], font_thickness=text_attr[TEXT_THICKNESS], font=font, text_color=(255, 255, 255))
        add_spacer += 1
        for clf_cnt, (clf_name, clf_results) in enumerate(frame_results.items()):
            if clf_results == 1:
                img = _put_text(img=img, text=clf_name, pos=(TextOptions.BORDER_BUFFER_Y.value, text_attr[SPACE_SCALE] * add_spacer), font_size=text_attr[FONT_SIZE], font_thickness=text_attr[TEXT_THICKNESS], font=font, text_color=TextOptions.COLOR.value)
                add_spacer += 1
        if video_setting:
            video_writer.write(img)
        if frame_setting:
            frame_save_name = os.path.join(frame_save_dir, f"{current_frm}.png")
            cv2.imwrite(frame_save_name, img)
        current_frm += 1
        print(f"Multi-processing video frame {current_frm} on core {group}...")

    cap.release()
    if video_setting:
        video_writer.release()
    return group


class PlotSklearnResultsMultiProcess(ConfigReader, TrainModelMixin, PlottingMixin):
    """
    Plot classification results on videos. Results are stored in the
    `project_folder/frames/output/sklearn_results` directory of the SimBA project.

    .. seealso::
       `Tutorial <https://github.com/sgoldenlab/simba/blob/master/docs/tutorial.md#step-10-sklearn-visualization__.
        For non-multiptocess class, see :meth:`simba.plotting.plot_clf_results.PlotSklearnResultsSingleCore`.

    .. image:: _static/img/sklearn_visualization.gif
       :width: 600
       :align: center

    :param Union[str, os.PathLike] config_path: path to SimBA project config file in Configparser format
    :param Optional[bool] video_setting: If True, SimBA will create compressed videos. Default True.
    :param Optional[bool] frame_setting: If True, SimBA will create individual frames. Default True.
    :param Optional[int] cores: Number of cores to use. Pass ``-1`` for all available cores.
    :param Optional[str] video_file_path: Path to video file to create classification visualizations for. If None, then all the videos in the csv/machine_results will be used. Default None.
    :param Optional[Union[Dict[str, float], bool]] text_settings: Dictionary holding the circle size, font size, spacing size, and text thickness of the printed text. If None, then these are autocomputed.
    :param Optional[bool] rotate: If True, the output video will be rotated 90 degrees from the input. Default False.
    :param Optional[str] palette: The name of the palette used for the pose-estimation key-points. Default ``Set1``.
    :param Optional[bool] print_timers: If True, the output video will have the cumulative time of the classified behaviours overlaid. Default True.

    :example:
    >>> text_settings = {'circle_scale': 5, 'font_size': 0.528, 'spacing_scale': 28, 'text_thickness': 2}
    >>> clf_plotter = PlotSklearnResultsMultiProcess(config_path='/Users/simon/Desktop/envs/simba/troubleshooting/beepboop174/project_folder/project_config.ini',
    >>>                                              video_setting=True,
    >>>                                              frame_setting=False,
    >>>                                              rotate=False,
    >>>                                              video_file_path='Trial    10.mp4',
    >>>                                              cores=5,
    >>>                                              text_settings=False)
    >>> clf_plotter.run()
    """

    def __init__(self,
                 config_path: Union[str, os.PathLike],
                 video_setting: Optional[bool] = True,
                 frame_setting: Optional[bool] = True,
                 cores: Optional[int] = -1,
                 video_file_path: Optional[str] = None,
                 text_settings: Optional[Union[Dict[str, float], bool]] = False,
                 palette: Optional[str] = 'Set1',
                 rotate: Optional[bool] = False,
                 print_timers: Optional[bool] = True):


        for i in [video_setting, frame_setting, rotate, print_timers]:
            check_valid_boolean(value=i, source=self.__class__.__name__, raise_error=True)
        if (not video_setting) and (not frame_setting):
            raise NoSpecifiedOutputError(msg="SIMBA ERROR: Please choose to create a video and/or frames. SimBA found that you ticked neither video and/or frames", source=self.__class__.__name__)
        check_int(name=f"{self.__class__.__name__} cores", value=cores, min_value=-1)
        if cores == -1: cores = find_core_cnt()[0]
        if not isinstance(text_settings, (bool)) and text_settings != None:
            check_if_keys_exist_in_dict(data=text_settings, key=TEXT_SETTING_KEYS)
        ConfigReader.__init__(self, config_path=config_path)
        TrainModelMixin.__init__(self)
        PlottingMixin.__init__(self)
        log_event(logger_name=str(__class__.__name__), log_type=TagNames.CLASS_INIT.value, msg=self.create_log_msg_from_init_args(locals=locals()))
        self.video_file_path, self.print_timers, self.text_settings = (video_file_path, print_timers, text_settings)
        self.video_setting, self.frame_setting, self.cores, self.rotate = (video_setting, frame_setting, cores, rotate,)
        if not os.path.exists(self.sklearn_plot_dir):
            os.makedirs(self.sklearn_plot_dir)
        self.pose_threshold = read_config_entry(self.config, ConfigKey.THRESHOLD_SETTINGS.value, ConfigKey.SKLEARN_BP_PROB_THRESH.value, Dtypes.FLOAT.value, 0.00)
        self.model_dict = self.get_model_info(self.config, self.clf_cnt)
        self.clf_colors = create_color_palette(pallete_name=palette, increments=self.clf_cnt)
        self.fourcc = cv2.VideoWriter_fourcc(*Formats.MP4_CODEC.value)
        if video_file_path is not None:
            check_file_exist_and_readable(os.path.join(self.video_dir, video_file_path))
            self.data_files = video_file_path

        # if platform.system() == "Darwin":
        #     multiprocessing.set_start_method("spawn", force=True)

    def __get_print_settings(self):
        self.text_attr = {}
        if (self.text_settings is False) or (self.text_settings is None):
            img_width, img_height = self.video_meta_data["width"], self.video_meta_data["height"]
            longest_str = max(['TIMERS:', 'ENSEMBLE PREDICTION:'] + self.clf_names, key=len)
            font_size, x_shift, y_shift = self.get_optimal_font_scales(text=longest_str, accepted_px_width=int(img_width / 3), accepted_px_height=int(img_width / 10), text_thickness=2)
            cirle_size = self.get_optimal_circle_size(frame_size=(img_width, img_height), circle_frame_ratio=100)
            self.text_attr[CIRCLE_SCALE] = cirle_size
            self.text_attr[FONT_SIZE] = font_size
            self.text_attr[SPACE_SCALE] = y_shift
            self.text_attr[TEXT_THICKNESS] = 2
        else:
            check_float(name="TEXT SIZE", value=self.text_settings[FONT_SIZE])
            check_int(name="SPACE SIZE", value=self.text_settings[SPACE_SCALE])
            check_int(name="TEXT THICKNESS", value=self.text_settings[TEXT_THICKNESS])
            check_int(name="CIRCLE SIZE", value=self.text_settings[CIRCLE_SCALE])
            self.text_attr[FONT_SIZE] = float(self.text_settings[FONT_SIZE])
            self.text_attr[SPACE_SCALE] = int(self.text_settings[SPACE_SCALE])
            self.text_attr[TEXT_THICKNESS] = int(self.text_settings[TEXT_THICKNESS])
            self.text_attr[CIRCLE_SCALE] = int(self.text_settings[CIRCLE_SCALE])

    def __index_df_for_multiprocessing(self, data: list) -> list:
        for cnt, df in enumerate(data):
            df["group"] = cnt
        return data

    def create_visualizations(self):
        video_timer = SimbaTimer(start=True)
        _, self.video_name, _ = get_fn_ext(self.file_path)
        self.data_df = read_df(self.file_path, self.file_type).reset_index(drop=True)
        self.video_settings, _, self.fps = self.read_video_info(video_name=self.video_name)
        self.video_path = self.find_video_of_file(self.video_dir, self.video_name)
        self.video_meta_data = get_video_meta_data(self.video_path)
        height, width = deepcopy(self.video_meta_data["height"]), deepcopy(self.video_meta_data["width"])
        self.video_frame_dir, self.video_temp_dir = None, None
        if self.frame_setting:
            self.video_frame_dir = os.path.join(self.sklearn_plot_dir, self.video_name)
            if not os.path.exists(self.video_frame_dir):
                os.makedirs(self.video_frame_dir)
        if self.video_setting:
            self.video_save_path = os.path.join(self.sklearn_plot_dir, self.video_name + ".mp4")
            self.video_temp_dir = os.path.join(self.sklearn_plot_dir, self.video_name, "temp")
            if not os.path.exists(self.video_temp_dir):
                os.makedirs(self.video_temp_dir)
        if self.rotate:
            self.video_meta_data["height"], self.video_meta_data["width"] = (width, height)
        self.__get_print_settings()

        for model in self.model_dict.values():
            self.data_df[model["model_name"] + "_cumsum"] = self.data_df[model["model_name"]].cumsum()
        self.data_df["index"] = self.data_df.index
        data = np.array_split(self.data_df, self.cores)
        frm_per_core = data[0].shape[0]

        data = self.__index_df_for_multiprocessing(data=data)
        with multiprocessing.Pool(self.cores, maxtasksperchild=self.maxtasksperchild) as pool:
            constants = functools.partial(_multiprocess_sklearn_video,
                                          clf_colors=self.clf_colors,
                                          bp_dict=self.animal_bp_dict,
                                          video_save_dir=self.video_temp_dir,
                                          frame_save_dir=self.video_frame_dir,
                                          models_info=self.model_dict,
                                          text_attr=self.text_attr,
                                          rotate=self.rotate,
                                          video_path=self.video_path,
                                          print_timers=self.print_timers,
                                          video_setting=self.video_setting,
                                          frame_setting=self.frame_setting,
                                          pose_threshold=self.pose_threshold)

            for cnt, result in enumerate(pool.imap(constants, data, chunksize=self.multiprocess_chunksize)):
                print("Image {}/{}, Video {}/{}...".format(str(int(frm_per_core * (result + 1))),
                                                           str(len(self.data_df)),
                                                           str(self.file_cnt + 1),
                                                           str(len(self.files_found))))
            if self.video_setting:
                print(f"Joining {self.video_name} multiprocessed video...")
                concatenate_videos_in_folder(in_folder=self.video_temp_dir, save_path=self.video_save_path)
            video_timer.stop_timer()
            pool.terminate()
            pool.join()
            print(f"Video {self.video_name} complete (elapsed time: {video_timer.elapsed_time_str}s)...")

    def run(self):
        if self.video_file_path is None:
            self.files_found = self.machine_results_paths
            print(f"Processing {len(self.machine_results_paths)} videos...")
            for file_cnt, file_path in enumerate(self.machine_results_paths):
                self.file_cnt, self.file_path = file_cnt, file_path
                self.create_visualizations()
        else:
            print("Processing 1 video...")
            self.file_cnt, file_path = 0, self.video_file_path
            _, file_name, _ = get_fn_ext(file_path)
            self.file_path = os.path.join(self.machine_results_dir, file_name + f".{self.file_type}")
            self.files_found = [self.file_path]
            check_file_exist_and_readable(self.file_path)
            self.create_visualizations()

        self.timer.stop_timer()
        if self.video_setting:
            stdout_success(msg=f"{len(self.files_found)} videos saved in {self.sklearn_plot_dir} directory", elapsed_time=self.timer.elapsed_time_str, source=self.__class__.__name__)
        if self.frame_setting:
            stdout_success(f"Frames for {len(self.files_found)} videos saved in sub-folders within {self.sklearn_plot_dir} directory", elapsed_time=self.timer.elapsed_time_str, source=self.__class__.__name__)


# if __name__ == "__main__":
#     clf_plotter = PlotSklearnResultsMultiProcess(config_path=r"C:\troubleshooting\mitra\project_folder\project_config.ini",
#                                                  video_setting=True,
#                                                  frame_setting=False,
#                                                  rotate=False,
#                                                  video_file_path='FR_gq_CNO_0621.mp4',
#                                                  cores=-1,
#                                                  text_settings=False)
#     clf_plotter.run()




#text_settings = {'circle_scale': 5, 'font_size': 0.528, 'spacing_scale': 28, 'text_thickness': 2}
# clf_plotter = PlotSklearnResultsMultiProcess(config_path='/Users/simon/Desktop/envs/simba/troubleshooting/beepboop174/project_folder/project_config.ini',
#                                              video_setting=True,
#                                              frame_setting=False,
#                                              rotate=False,
#                                              video_file_path='592_MA147_Gq_CNO_0515.mp4',
#                                              cores=-1,
#                                              text_settings=False)
# clf_plotter.run()
#

# clf_plotter = PlotSklearnResultsMultiProcess(config_path='/Users/simon/Desktop/envs/troubleshooting/DLC_2_Black_animals/project_folder/project_config.ini', video_setting=True, frame_setting=False, rotate=False, video_file_path='Together_1.avi', cores=5)
# clf_plotter.run()
