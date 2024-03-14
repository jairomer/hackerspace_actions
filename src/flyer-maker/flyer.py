from PIL import Image


class FlyerData:
    def __init__(self, title, subtitle, date, timeframe, place, metro):
        self.title = title
        self.subtitle = subtitle 
        self.date = date
        self.timeframe = timeframe 
        self.place = place
        self.metro = metro

class FlyerDimensions:
    def __init__(self, size):
        self.y_percent = 10
        self.x_percent = 10
        self.x_increment_percent = 15
        self.fontsize_small_percent = 4
        self.fontsize_large_percent = 8
        
        if Flyer.isPortrait(size):
            # Portrait percentages
            self.x_percent = 15
            self.y_percent = 5
            self.x_increment_percent = 10
            self.fontsize_small_percent = 7
            self.fontsize_large_percent = 10

        self.ytxt = Flyer.width(size, self.y_percent)
        self.xtxt = Flyer.heigh(size, self.x_percent)
        self.xincrements = Flyer.heigh(size, self.flyer_dimensions.x_increment_percent)
        self.yincrements = 0
        self.fontsize_small = Flyer.width(size, self.flyer_dimensions.fontsize_small_percent)
        self.fontsize_large = Flyer.width(size, self.flyer_dimensions.fontsize_large_percent)

    def increment_xposition(self, xinc=None):
        if xinc == None:
            self.xtxt += self.xincrements
        else:
            self.xtxt += xinc
    
    def increment_yposition(self, yinc=None):
        if yinc == None:
            self.ytxt += self.yincrements
        else:
            self.ytxt += yinc

    def get_position(self) -> tuple:
        return (self.xtxt, self.ytxt)
 
class Flyer(Image):
    WIDTH=0
    HEIGH=1
    
    @staticmethod
    def get_dimensions(size) -> FlyerDimensions:
        return FlyerDimensions(size)

    @staticmethod
    def width(size: tuple, percent: float) -> int: return int(size[Flyer.WIDTH] * percent/100)
    
    @staticmethod
    def heigh(size: tuple, percent: float) -> int: return int(size[Flyer.HEIGH] * percent/100)
    
    @staticmethod
    def resize_factor(size, factor): return (int(size[Flyer.WIDTH]*factor), int(size[Flyer.HEIGH]*factor))
    
    @staticmethod
    def isPortrait(size): return size[Flyer.WIDTH] <= size[Flyer.HEIGH]

