from PIL import Image, ImageDraw

from flyer import Flyer, FlyerData
from fonts import ubuntu_regular 

def make_flyer_from_image(flyer_data: FlyerData, base : Image, metro_path=None) -> Flyer:
    """
    Given flyer data and a PIL.Image to use as background, put the data on the background after applying a dark overlay.
    """
    dark_overlay = Image.new("RGBA", base.size, (0,0,0,128))
    bg = Image.alpha_composite(base, dark_overlay)
    img = ImageDraw.Draw(bg) 
   
    flyerseeker = Flyer.get_dimensions(base.size)
    
    # Add title
    img.multiline_text(flyerseeker.get_position(), flyer_data.title, align="center", font=ubuntu_regular(flyerseeker.fonstsize_large), fill=(255,255,255,255))
    flyerseeker.increment_xposition()

    # Add Subtitle
    img.multiline_text(flyerseeker.get_position(), flyer_data.subtitle, align="center", font=ubuntu_regular(flyerseeker.fonstsize_small), fill=(255,255,255,255))
    flyerseeker.increment_xposition()

    # Add Date
    img.multiline_text(flyerseeker.get_position(), flyer_data.date, align="center", font=ubuntu_regular(flyerseeker.fonstsize_large), fill=(255,255,255,255))
    flyerseeker.increment_xposition()

    # Add Time frame
    img.multiline_text(flyerseeker.get_position(), flyer_data.timeframe, align="center", font=ubuntu_regular(flyerseeker.fonstsize_small), fill=(255,255,255,255))
    flyerseeker.increment_xposition()

    # Add place
    img.multiline_text(flyerseeker.get_position(), flyer_data.place, align="center", font=ubuntu_regular(flyerseeker.fonstsize_large), fill=(255,255,255,255))
    flyerseeker.increment_xposition()
    
    if metro_path != None:
        # Add metro
        metro_logo = Image.open(metro_path)
        # Obtain scale ratio according to scaled font height
        scale_ratio = flyerseeker.fontsize_small/metro_logo.size[Flyer.HEIGH]
        metro_logo = metro_logo.resize(Flyer.resize_factor(metro_logo.size, scale_ratio))
        bg.alpha_composite(metro_logo, (flyerseeker.ytxt, flyerseeker.xtxt))
        flyerseeker.increment_yposition(metro_logo.size[Flyer.WIDTH])
        img.multiline_text(flyerseeker.get_position(), flyer_data.metro, align="center", font=ubuntu_regular(flyerseeker.fonstsize_small), fill=(255,255,255,255))

    return bg
