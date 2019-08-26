import numpy as np
from InputReader import Simple_Input_Reader


class ToTimeSeries:
    def __init__(self, x_size, y_size, **kwargs):
        if kwargs.get('file_name', None):
            self.file_name = kwargs.get('file_name')
        else:
            self.file_name = 't1.avi'

        self._input_reader = Simple_Input_Reader()
        self.original_file, self.frame_count, self.single_frame_width, self.single_frame_height = self._input_reader.input_to_np(input_location=self.file_name, grouped_frames=1)
        self.bin_x_size = x_size
        self.bin_y_size = y_size
        self.bin_size = int(self.bin_x_size * self.bin_y_size)
        self.single_frame_size = int(self.single_frame_width * self.single_frame_height)
        self.number_of_bins = int(self.single_frame_size / self.bin_size)

    def into_time_series(self):
        time_series_of_bins = np.zeros([self.number_of_bins, self.frame_count, self.bin_y_size, self.bin_x_size, 3], dtype=int)
        frames_amount = self.frame_count
        x_min = 0
        x_max = self.bin_x_size
        y_min = 0
        y_max = self.bin_y_size
        bin_to_slice_index = 0
        while bin_to_slice_index < self.number_of_bins:
            x_indices = list()
            for i in range(x_min, x_max):
                x_indices.append(i)
            #     runs on each frame
            for i in range(0, frames_amount):
                time_series_of_bins[bin_to_slice_index, i] = self.original_file[i][y_min:y_max, x_indices]

            x_min = x_max
            x_max = x_max + x_min

            if x_max - self.single_frame_width >= 0:
                x_min = 0
                x_max = self.bin_x_size
                y_min = y_max
                y_max = y_max + y_min

            bin_to_slice_index += 1

        return time_series_of_bins

