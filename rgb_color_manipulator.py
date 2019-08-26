from abc import ABC, abstractmethod
from InputReader import Simple_Input_Reader


class Abstract_Color_Manipulator(ABC):

    @abstractmethod
    def manipulate_pixel(self, rgb_to_manipulate):
        pass

    def manipulate_frame(self, frame):
        for i in range(len(frame)):
            for j in range(len(frame[i])):
                frame[i][j] = self.manipulate_pixel(frame[i][j])
        return frame.copy()

    def manipulate_video(self, video):
        for i in range(len(video)):
            video[i] = self.manipulate_frame(video[i])
        return video

class Simple_Comparison_Manipulator(Abstract_Color_Manipulator):

    def __init__(self, new_color, comperator, **kwargs):
        '''

        :param new_color: new color to return in case of change
        :param comperator: comperator used to check if need to change rgb
        :param kwargs: deep_copy_return_values, True if deep copy of return value is desired, False if shallow copy. default is false
        '''
        self.deep_copy_return_values = False if kwargs.get('deep_copy_return_values', None) else kwargs.get('deep_copy_return_values')
        self._new_color = new_color
        self._comperator = comperator

    def manipulate_pixel(self, rgb_to_manipulate):
        if self._comperator.need_to_change(rgb_to_manipulate):
            to_return = self._new_color
        else:
            to_return = rgb_to_manipulate
        return to_return.copy() if self.deep_copy_return_values else to_return


    def get_new_color(self):
        return self._new_color

    def get_comperator(self):
        return self._comperator

    def set_new_color(self, new_color):
        self._new_color=new_color

    def set_comperator(self, comperator):
        self._comperator=comperator

    def __str__(self):
        return 'simple color comperator:\nnew color: [{},{},{}]\ncomperator: {}'.format(self._new_color[0],self._new_color[1],self._new_color[2],str(self._comperator))


class Comperator(ABC):

    @abstractmethod
    def need_to_change(self, rgb_to_change):
        pass

class In_All_Ranges_Comperator(Comperator):


    @staticmethod
    def _validate_ranges(*args):
        for arg in args:
            if not isinstance(arg,range):
                raise Exception('the range {}, is not a valid range'.format(str(arg)))

    def __init__(self, r_range, g_range, b_range):
        self._validate_ranges(r_range,g_range,b_range)
        self.r_range = r_range
        self.g_range = g_range
        self.b_range = b_range
    def need_to_change(self, rgb_to_change):
        return ((rgb_to_change[0] in self.r_range) and (rgb_to_change[1] in self.g_range) and (rgb_to_change[2] in self.b_range))

    def __str__(self):
        return 'In all Range Comperator: range red - [{},{}]; range green - [{},{}]; range blue - [{},{}]'.\
            format(self.r_range[0], self.r_range[1], self.g_range[0], self.g_range[1], self.b_range[0],self.b_range[1])


def read_video(video_location, **kwargs):
    new_color = kwargs.get('new_color', None)
    ir = Simple_Input_Reader()
    video_frames, frames_amount, frame_width, frame_height = ir.input_to_np(video_location, 1 if kwargs.get('grouped_frames') is None else kwargs.get('grouped_frames'))

    if new_color is None:
        return video_frames, frames_amount, frame_width, frame_height
    else:
        ranges = [range(0, 0), range(0, 0), range(0, 0)] if kwargs.get('ranges', None) is None else kwargs.get('ranges')
        comperator = In_All_Ranges_Comperator(ranges[0],ranges[1],ranges[2]) if kwargs.get('comperator', None) is None else kwargs.get('comperator')
        manipulator = Simple_Comparison_Manipulator(new_color,comperator) if kwargs.get('manipulator',None) is None else kwargs.get('manipulator')
        return manipulator.manipulate_video(video_frames), frames_amount, frame_width, frame_height


