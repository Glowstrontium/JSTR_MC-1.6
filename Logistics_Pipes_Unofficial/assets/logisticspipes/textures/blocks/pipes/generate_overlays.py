#
# Logistics Pipes overlay compositor
#
# Requires Python Imaging Library (http://pythonware.com/products/pil/)
#
# Author: Leenhaart (https://github.com/Leenhaart/)
# License: Free for public use, modification and redistribution
#

# Usage: Run from pipes directory
#
# This program combines images from the 'original' directory and the
# 'status_overlay' directory to create the composited textures required
# by the Logistics Pipes mod.


import os
import Image



def getBaseTexturePaths(src_base):
    """Find paths to base versions of pipe textures."""
    files = [map(lambda y: os.path.join(x[0], y), x[2]) for x in os.walk(src_base)]
    
    paths = []
    map(paths.extend, files)
    return filter(lambda x: x.endswith('.png'), paths)

def getBaseDirs(src_base):
    """Find directories in the source tree."""
    dirs = [map(lambda y: os.path.join(x[0], y), x[1]) for x in os.walk(src_base)]
    paths = []
    map(paths.extend, dirs)
    return paths

def buildDestPaths(src_base, dest_base):
    """Creates a directory structure that mirrors the source tree."""
    for d in getBaseDirs(src_base):
        dest = os.path.join(dest_base, os.path.relpath(d, src_base))
        if not os.path.exists(dest):
            os.mkdir(dest)

    for p in getBaseTexturePaths(src_base):
        name = os.path.relpath(p, src_base)[:-4]
        dest = os.path.join(dest_base, name)
        if not os.path.exists(dest):
            os.mkdir(dest)

def loadOverlays(src, overlay_list):
    """Load overlay textures into a map { final_name -> Image }."""
    overlay_map = {}
    for x in overlay_list:
        im = Image.open(os.path.join(src, x)).convert('RGBA')
        overlay_map[x] = im
    return overlay_map
        
def genOverlays(src, dest, overlay_map):
    """Apply overlays to a single pipe and save to correct destination."""
    im = Image.open(src).convert('RGBA')
    im.save(os.path.join(dest, 'un-overlayed.png'))
    
    for over in overlay_map:
        im_overlay = overlay_map[over]

        if im.size == im_overlay.size:
            # Paste overlay with alpha
            im_composite = im.copy()
            im_composite.paste(im_overlay, im_overlay)
            im_composite.save(os.path.join(dest, over))
        else:
            print 'Unable to composite %s due to different texture sizes.' % src



##
print 'Logistics Pipes overlay compositor (unofficial version by Leenhaart)'
##

src_path = 'original'
dest_path = 'overlay_gen'

##
print 'Building overlay directories...'
##

if not os.path.exists(dest_path):
    os.mkdir(dest_path)

buildDestPaths(src_path, dest_path)

##        
print 'Applying standard power overlays...'
##

overlays = loadOverlays('status_overlay', ['powered-pipe.png', 'un-powered-pipe.png'])

for p in getBaseTexturePaths(src_path):
    name = os.path.relpath(p, src_path)[:-4]
    dest = os.path.join(dest_path, name)
    genOverlays(p, dest, overlays)


print 'Completed.'
raw_input('Press ENTER to close')
