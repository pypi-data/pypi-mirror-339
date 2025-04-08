__author__ = "Simon Nilsson"

import multiprocessing
import os
from tkinter import *
from typing import Union

import numpy as np

from simba.mixins.config_reader import ConfigReader
from simba.mixins.pop_up_mixin import PopUpMixin
from simba.plotting.heat_mapper_clf import HeatMapperClfSingleCore
from simba.plotting.heat_mapper_clf_mp import HeatMapperClfMultiprocess
from simba.ui.tkinter_functions import (CreateLabelFrameWithIcon, DropDownMenu,
                                        SimbaButton, SimbaCheckbox)
from simba.utils.checks import check_if_filepath_list_is_empty
from simba.utils.enums import Formats, Keys, Links, Paths
from simba.utils.read_write import get_file_name_info_in_directory


class HeatmapClfPopUp(PopUpMixin, ConfigReader):
    """
    :example:
    >>> _ = HeatmapClfPopUp(config_path=r"C:\troubleshooting\RAT_NOR\project_folder\project_config.ini")
    """

    def __init__(self, config_path: Union[str, os.PathLike]):
        ConfigReader.__init__(self, config_path=config_path, read_video_info=False)
        self.data_path = os.path.join(self.project_path, Paths.MACHINE_RESULTS_DIR.value)

        self.files_found_dict = get_file_name_info_in_directory(directory=self.data_path, file_type=self.file_type)
        check_if_filepath_list_is_empty( filepaths=list(self.files_found_dict.keys()), error_msg="SIMBA ERROR: Zero files found in the project_folder/csv/machine_results directory. ",)
        PopUpMixin.__init__(self, title="CREATE CLASSIFICATION HEATMAP PLOTS", icon='heatmap')

        max_scales = list(np.linspace(5, 600, 5))
        max_scales.insert(0, "Auto-compute")

        self.style_settings_frm = CreateLabelFrameWithIcon(parent=self.main_frm, header="STYLE SETTINGS", icon_name=Keys.DOCUMENTATION.value, icon_link=Links.HEATMAP_CLF.value,)
        self.palette_dropdown = DropDownMenu(self.style_settings_frm, "Palette:", self.palette_options, "16")
        self.shading_dropdown = DropDownMenu(self.style_settings_frm, "Shading:", self.shading_options, "16")
        self.clf_dropdown = DropDownMenu(self.style_settings_frm, "Classifier:", self.clf_names, "16")
        self.bp_dropdown = DropDownMenu(self.style_settings_frm, "Body-part:", self.body_parts_lst, "16")
        self.max_time_scale_dropdown = DropDownMenu(self.style_settings_frm, "Max time scale (s):", max_scales, "16")
        self.bin_size_dropdown = DropDownMenu(self.style_settings_frm, "Bin size (mm):", self.heatmap_bin_size_options, "16",)

        self.palette_dropdown.setChoices(self.palette_options[0])
        self.shading_dropdown.setChoices(self.shading_options[0])
        self.clf_dropdown.setChoices(self.clf_names[0])
        self.bp_dropdown.setChoices(self.body_parts_lst[0])
        self.max_time_scale_dropdown.setChoices(max_scales[0])
        self.bin_size_dropdown.setChoices("80×80")

        self.settings_frm = LabelFrame(self.main_frm,text="VISUALIZATION SETTINGS",font=Formats.FONT_HEADER.value,pady=5,padx=5,)
        self.multiprocessing_var = BooleanVar()

        heatmap_frames_cb, self.heatmap_frames_var = SimbaCheckbox(parent=self.settings_frm, txt='CREATE FRAMES', txt_img='frames')
        heatmap_videos_cb, self.heatmap_videos_var = SimbaCheckbox(parent=self.settings_frm, txt='CREATE VIDEOS', txt_img='video')
        heatmap_last_frm_cb, self.heatmap_last_frm_var = SimbaCheckbox(parent=self.settings_frm, txt='CREATE LAST FRAME', txt_img='finish')

        self.multiprocess_cb = Checkbutton(
            self.settings_frm,
            text="Multiprocess videos (faster)",
            font=Formats.FONT_REGULAR.value,
            variable=self.multiprocessing_var,
            command=lambda: self.enable_dropdown_from_checkbox(
                check_box_var=self.multiprocessing_var,
                dropdown_menus=[self.multiprocess_dropdown],
            ),
        )
        self.multiprocess_dropdown = DropDownMenu(self.settings_frm, "CPU cores:", list(range(2, self.cpu_cnt)), "12")
        self.multiprocess_dropdown.setChoices(2)
        self.multiprocess_dropdown.disable()

        self.run_frm = LabelFrame(self.main_frm, text="RUN", font=Formats.FONT_HEADER.value, pady=5, padx=5, fg="black",)
        self.run_single_video_frm = LabelFrame(self.run_frm, text="SINGLE VIDEO", font=Formats.FONT_HEADER.value, pady=5, padx=5, fg="black",)

        self.run_single_video_btn = SimbaButton(parent=self.run_single_video_frm, txt="Create single video", txt_clr="blue", img='rocket', font=Formats.FONT_REGULAR.value, cmd=self.__create_heatmap_plots, cmd_kwargs={'multiple_videos': False})
        self.single_video_dropdown = DropDownMenu(self.run_single_video_frm, "Video:", list(self.files_found_dict.keys()), "12",)
        self.single_video_dropdown.setChoices(list(self.files_found_dict.keys())[0])
        self.run_multiple_videos = LabelFrame(self.run_frm, text="MULTIPLE VIDEO", font=Formats.FONT_HEADER.value, pady=5, padx=5, fg="black",)

        self.run_multiple_video_btn = SimbaButton(parent=self.run_multiple_videos, txt="Create multiple videos ({} video(s) found)".format(str(len(list(self.files_found_dict.keys())))), img='rocket', txt_clr="blue", font=Formats.FONT_REGULAR.value, cmd=self.__create_heatmap_plots, cmd_kwargs={'multiple_videos': True})
        self.style_settings_frm.grid(row=0, sticky=NW)
        self.palette_dropdown.grid(row=0, sticky=NW)
        self.shading_dropdown.grid(row=1, sticky=NW)
        self.clf_dropdown.grid(row=2, sticky=NW)
        self.bp_dropdown.grid(row=3, sticky=NW)
        self.max_time_scale_dropdown.grid(row=4, sticky=NW)
        self.bin_size_dropdown.grid(row=5, sticky=NW)

        self.settings_frm.grid(row=1, sticky=NW)
        heatmap_frames_cb.grid(row=0, sticky=NW)
        heatmap_videos_cb.grid(row=1, sticky=NW)
        heatmap_last_frm_cb.grid(row=2, sticky=NW)
        self.multiprocess_cb.grid(row=3, column=0, sticky=NW)
        self.multiprocess_dropdown.grid(row=3, column=1, sticky=NW)

        self.run_frm.grid(row=2, sticky=NW)
        self.run_single_video_frm.grid(row=0, sticky=NW)
        self.run_single_video_btn.grid(row=0, column=0, sticky=NW)
        self.single_video_dropdown.grid(row=0, column=1, sticky=NW)

        self.run_multiple_videos.grid(row=1, sticky=NW)
        self.run_multiple_video_btn.grid(row=0, sticky=NW)

        self.main_frm.mainloop()

    def __create_heatmap_plots(self, multiple_videos: bool):
        if multiple_videos:
            data_paths = list(self.files_found_dict.values())
        else:
            data_paths = [
                self.files_found_dict[self.single_video_dropdown.getChoices()]
            ]

        if self.max_time_scale_dropdown.getChoices() != "Auto-compute":
            max_scale = int(self.max_time_scale_dropdown.getChoices().split("×")[0])
        else:
            max_scale = "auto"

        bin_size = int(self.bin_size_dropdown.getChoices().split("×")[0])

        style_attr = {
            "palette": self.palette_dropdown.getChoices(),
            "shading": self.shading_dropdown.getChoices(),
            "max_scale": max_scale,
            "bin_size": bin_size,
        }

        if not self.multiprocessing_var.get():
            heatmapper_clf = HeatMapperClfSingleCore(
                config_path=self.config_path,
                style_attr=style_attr,
                final_img_setting=self.heatmap_last_frm_var.get(),
                video_setting=self.heatmap_videos_var.get(),
                frame_setting=self.heatmap_frames_var.get(),
                bodypart=self.bp_dropdown.getChoices(),
                data_paths=data_paths,
                clf_name=self.clf_dropdown.getChoices(),
            )

            heatmapper_clf_processor = multiprocessing.Process(heatmapper_clf.run())
            heatmapper_clf_processor.start()

        else:
            heatmapper_clf = HeatMapperClfMultiprocess(
                config_path=self.config_path,
                style_attr=style_attr,
                final_img_setting=self.heatmap_last_frm_var.get(),
                video_setting=self.heatmap_videos_var.get(),
                frame_setting=self.heatmap_frames_var.get(),
                bodypart=self.bp_dropdown.getChoices(),
                data_paths=data_paths,
                clf_name=self.clf_dropdown.getChoices(),
                core_cnt=int(self.multiprocess_dropdown.getChoices()),
            )

            heatmapper_clf.run()



