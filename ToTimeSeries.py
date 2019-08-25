import numpy as np
import cv2
from InputReader import read_file
from SimpleVisualizationTool import simpleVisualization as SV


file, frameCount, frameWidth, frameHeight = read_file('t1.avi')

class ToTimeSeries():
    def __init__(self, file, x_size, y_size, frame_count, frame_height, frame_width):
        self.original_file = file
        self.frame_number = frame_count
        self.bin_x_size = x_size
        self.bin_y_size = y_size
        self.bin_size = int(self.bin_x_size * self.bin_y_size)
        self.single_frame_width = frame_width
        self.single_frame_height = frame_height
        self.single_frame_size = int(frame_width * frame_height)
        self.number_of_bins = int(self.single_frame_size / self.bin_size)
        # np.empty([self.number_of_cells, self.frame_number, self.cell_y_size, self.cell_x_size])

    def into_time_series(self):
        time_series_of_bins = np.zeros([self.number_of_bins, self.frame_number, self.bin_y_size, self.bin_x_size, 3], dtype=int)
        frame_number = self.frame_number
        ans = list()
        x_min = 0
        x_max = self.bin_x_size
        y_min = 0
        y_max = self.bin_y_size
        bin_to_slice_index = 0
        while(bin_to_slice_index < self.number_of_bins):
            x_indices = list()
            for i in range(x_min, x_max):
                x_indices.append(i)
            #     runs on each frame
            for i in range(0, frame_number):
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


tts = ToTimeSeries(file=file, x_size=90, y_size=90, frame_count=70, frame_height=frameHeight, frame_width=frameWidth)
result = tts.into_time_series()
bin_num = 1
frame_num = 60
print(result[bin_num][frame_num][0][0])
video = result[bin_num]
SV = SV()
SV.visualize_video(video=video, frame_update_frequncy=0.2, gray=False, frame_title='test title')


