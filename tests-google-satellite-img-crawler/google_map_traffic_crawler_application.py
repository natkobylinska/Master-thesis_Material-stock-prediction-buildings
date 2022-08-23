import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import numpy as np

# png to img function (N)
def png_bin_to_image_array(png):
    '''
    png binary to image
    '''
    img = cv2.imdecode(np.asarray(bytearray(png)),cv2.IMREAD_COLOR)
    return img
    
# geo-functions
import math

def geo_destination(latlon, brng, d):
    '''
    latlon: lat and lon of start point; as a list (N)
    
    brng: bering in degree (0 north, 90 east, 180 south, 270 west)
    
    d: distance in km
    '''
    R = 6378.137 #equatorial radius
    brng = math.radians(brng)
    
    lat1 = math.radians(latlon[0]) #Current lat point converted to radians
    lon1 = math.radians(latlon[1]) #Current long point converted to radians

    lat2 = math.asin(math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    
    return (lat2,lon2) # why do I need it? (N)

def geo_disk_bound(latlon, r):
    '''
    return the geo bounding box of a geo-disk in the format of [lat_min,lat_max,lon_min,lon_max]
    
    r: radius of the geo-disk in km
    '''
    n = geo_destination(latlon,0,r)
    s = geo_destination(latlon,180,r)
    w = geo_destination(latlon,270,r)
    e = geo_destination(latlon,90,r)

    return [s[0],n[0],w[1],e[1]]

def geo_grid(latlon, r, num):
    lat_min, lat_max, lon_min, lon_max = geo_disk_bound(latlon, r)
    lat_range = lat_max-lat_min
    lon_range = lon_max-lon_min
    return [[(i,j),(lat_range*j/num+lat_min,lon_range*i/num+lon_min)] for j in range(num+1) for i in range(num+1)]

def geo_dist(latlon1,latlon2):
    R = 6378.137 #equatorial radius
    
    lat1 = math.radians(latlon1[0]) #Current lat point converted to radians
    lon1 = math.radians(latlon1[1]) #Current long point converted to radians
    lat2 = math.radians(latlon2[0]) #Current lat point converted to radians
    lon2 = math.radians(latlon2[1]) #Current long point converted to radians

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
    
def m_per_pixel(latlon, zoom):
    '''
    meter per pixel at certain zoom level
    see https://gis.stackexchange.com/questions/7430/what-ratio-scales-do-google-maps-zoom-levels-correspond-to
    '''
    metersPerPx = 156543.03392 * math.cos(math.radians(latlon[0])) / math.pow(2, zoom)
    return metersPerPx

# geo-tiles by center and lat-lon coord
def geo_tiles_by_radius(latlon, radius, map_zoom, image_w_pixel, image_h_pixel, chrome_zoom):
    '''
    create a grid for screen shotting based on the settings of web browser and system display
    
    latlon: location
    radius: geo_disk radius, in km
    map_zoom: from 0 to 19, google map zoom level
    image_w_pixel: target image size
    image_h_pixel: target image size
    chrome_zoom: zoom (scaling) level of google chrome
    '''
    tile_w_pixel=image_w_pixel/chrome_zoom
    tile_h_pixel=image_h_pixel/chrome_zoom
    
    mppixel=m_per_pixel(latlon, map_zoom) # m per pixel
    #print('m per pixel',mppixel)
    #print('display pixel',tile_w_pixel,'x',tile_h_pixel)
    
    patch_km_x = tile_w_pixel*mppixel*0.001
    patch_km_y = tile_h_pixel*mppixel*0.001

    # from radius to diameter
    patch_num_x=max(1,round(2*radius/patch_km_x))
    patch_num_y=max(1,round(2*radius/patch_km_y))

    range_x = patch_num_x*patch_km_x
    range_y = patch_num_y*patch_km_y
    
    #print('patch size',patch_km_x,'x',patch_km_y,'km, patch num',patch_num_x,',',patch_num_y)

    n = geo_destination(latlon,0,range_y/2)
    s = geo_destination(latlon,180,range_y/2)
    w = geo_destination(latlon,270,range_x/2)
    e = geo_destination(latlon,90,range_x/2)

    lat_min, lat_max, lon_min, lon_max = [s[0],n[0],w[1],e[1]]
    lat_range = lat_max-lat_min
    lon_range = lon_max-lon_min
    
    return {'center_latlon':latlon,
            'map_zoom':map_zoom, # zoom level of google map
            'tiles_ij_latlon':[[(i,j),(lat_range*(j+0.5)/patch_num_y+lat_min,lon_range*(i+0.5)/patch_num_x+lon_min)] for j in range(patch_num_y) for i in range(patch_num_x)],
            'bounding_box':[s[0],n[0],w[1],e[1]], # bounding box of all tiles
            'tile_number_xy':[patch_num_x,patch_num_y], # number of tiles in x and y directions
            'tile_size_km_xy':[patch_km_x,patch_km_y], # size of each tiles in km
            'tile_size_pixel':[tile_w_pixel,tile_h_pixel], # size of each tiles in pixel (the virtual size affected by the chrome zoom level)
            'image_size_pixel':[image_w_pixel,image_h_pixel]} # size of each tiles in pixel (the screen shot size)

def geo_tiles_by_bbox(bbox, map_zoom, image_w_pixel, image_h_pixel, chrome_zoom):
    '''
    create a grid for screen shotting based on the settings of web browser and system display
    
    bbox: latmin latmax lonmin lonmax
    map_zoom: from 0 to 19, google map zoom level
    image_w_pixel: target image size
    image_h_pixel: target image size
    chrome_zoom: zoom (scaling) level of google chrome
    '''
    tile_w_pixel=image_w_pixel/chrome_zoom
    tile_h_pixel=image_h_pixel/chrome_zoom
    
    latlon=((bbox[0]+bbox[1])/2,(bbox[2]+bbox[3])/2)
    
    geo_dist_x = geo_dist([latlon[0],bbox[2]],[latlon[0],bbox[3]]) # lat-mid, lon-min, lat-mid,lon-max
    geo_dist_y = geo_dist([bbox[0],latlon[1]],[bbox[1],latlon[1]]) # lat-min, lon-mid, lat-max,lon-mid
    
    mppixel=m_per_pixel(latlon, map_zoom) # m per pixel
    #print('m per pixel',mppixel)
    #print('display pixel',tile_w_pixel,'x',tile_h_pixel)
    
    patch_km_x = tile_w_pixel*mppixel*0.001
    patch_km_y = tile_h_pixel*mppixel*0.001

    # from radius to diameter
    patch_num_x=max(1,round(geo_dist_x/patch_km_x))
    patch_num_y=max(1,round(geo_dist_y/patch_km_y))

    range_x = patch_num_x*patch_km_x
    range_y = patch_num_y*patch_km_y
    
    #print('patch size',patch_km_x,'x',patch_km_y,'km, patch num',patch_num_x,',',patch_num_y)

    n = geo_destination(latlon,0,range_y/2)
    s = geo_destination(latlon,180,range_y/2)
    w = geo_destination(latlon,270,range_x/2)
    e = geo_destination(latlon,90,range_x/2)

    lat_min, lat_max, lon_min, lon_max = [s[0],n[0],w[1],e[1]]
    lat_range = lat_max-lat_min
    lon_range = lon_max-lon_min
    
    return {'center_latlon':latlon,
            'map_zoom':map_zoom, # zoom level of google map
            'tiles_ij_latlon':[[(i,j),(lat_range*(j+0.5)/patch_num_y+lat_min,lon_range*(i+0.5)/patch_num_x+lon_min)] for j in range(patch_num_y) for i in range(patch_num_x)],
            'bounding_box':[s[0],n[0],w[1],e[1]], # bounding box of all tiles
            'tile_number_xy':[patch_num_x,patch_num_y], # number of tiles in x and y directions
            'tile_size_km_xy':[patch_km_x,patch_km_y], # size of each tiles in km
            'tile_size_pixel':[tile_w_pixel,tile_h_pixel], # size of each tiles in pixel (the virtual size affected by the chrome zoom level)
            'image_size_pixel':[image_w_pixel,image_h_pixel]} # size of each tiles in pixel (the screen shot size)

# chrome driver
def start_chrome_driver(chrome_zoom=1,pos=None):
    '''
    start a chrome driver
    '''
    #chrome_options = Options()
    #chrome_options.add_argument("--window-size=1000,600" # specified window size
    #chrome_options.add_argument("--kiosk") # full-screen
    #chrome_options.add_argument("start-maximized") # maximized
    #driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome()
    
    # change screen
    if pos is not None:
        driver.set_window_position(pos, 0)

    if chrome_zoom != 1:
        driver.get('chrome://settings/')
        driver.execute_script('chrome.settingsPrivate.setDefaultZoom('+str(chrome_zoom)+');')
    return {'driver':driver,'chrome_zoom':chrome_zoom}

# crawl data using given driver on given tiles
import os

MAP=''
MAP_TRAFFIC='/data=!5m1!1e1'
SATELLITE='/data=!3m1!1e3'
TERRAIN='/data=!5m1!1e4'
TERRAIN_TRAFFIC='/data=!5m2!1e1!1e4'

def crawl_map_tiles(chrome_driver, tiles, path, sys_disp_scale, data=MAP_TRAFFIC, win_buf_w=50, win_buf_h=400, delay=0, delay_between_tiles=0):
    '''
    crawl google map tiles
    
    chrome_driver: {driver, chrome_zoom}
    tiles: tiles generated by geo_tiles
    path: path to save the png files
    sys_disp_scale: system display scale, e.g. windows have 150% scale on retina screen
    data: what data to collect. see MAP, MAP_TRAFFIC, SATELLITE, TERRAIN and TERRAIN_TRAFFIC
    win_buf_w, win_buf_h: additional windows size for making sufficient screen shot
    delay: waiting time (seconds) before taking screen shot
    '''
    chrome_zoom=chrome_driver['chrome_zoom']
    driver=chrome_driver['driver']
    
    image_w_pixel,image_h_pixel=tiles['image_size_pixel']
    map_zoom=tiles['map_zoom']
    
    # adjust size
    driver.set_window_size(image_w_pixel+win_buf_w, image_h_pixel+win_buf_h)

    # actual output size (affected by system display scale)
    image_w_sys_scale = int(image_w_pixel*sys_disp_scale)
    image_h_sys_scale = int(image_h_pixel*sys_disp_scale)
    
    # return
    # go to the map
    for index,coord in tiles['tiles_ij_latlon']:
        lat,lon=coord
        x,y=index
        coord_str=str(lat)+','+str(lon)
        driver.get('https://www.google.ch/maps/@'+coord_str+','+str(map_zoom)+'z'+data);
        
        if delay>0:
            time.sleep(delay)
            
        png = driver.get_screenshot_as_png()
        file=os.path.join(path,str(x)+','+str(y)+'.png')

        image = png_bin_to_image_array(png)
        h,w=image.shape[:2]
        w=(w-image_w_sys_scale)//2
        h=(h-image_h_sys_scale)//2
        cv2.imwrite(file,image[h:h+image_h_sys_scale,w:w+image_w_sys_scale,...])
        
        if delay_between_tiles>0:
            time.sleep(delay_between_tiles)
    #with open(os.path.join(path,'tiles.json'), 'w') as f:
    #    json.dump(tiles, f)

from datetime import datetime
import json

def default_conf(file):
    config={'SYSTEM_DISPLAY_SCALING':1.0,
          'CHROME_ZOOM':1.0,
          'MAP_ZOOM':15,
          'IMAGE_W':1000,
          'IMAGE_H':800,
          'DELAY_SEC_BETWEEN_BBOX':10,
          'DELAY_SEC_BETWEEN_TILE':1,
          'WINDOW_POS_X':0,
          'WINDOW_POS_Y':0
          }
    with open(file,'w') as f:
        json.dump(config,f)

PATH = os.path.split(os.path.abspath(__file__))[0]
#print(PATH)

def makesure_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_tile_file(bbox_file, config_file, targe_file):
    with open(config_file,'r') as f:
        config=json.load(f)
        
    MAP_ZOOM = config['MAP_ZOOM']
    IMAGE_W = config['IMAGE_W']
    IMAGE_H = config['IMAGE_H']
    
    CHROME_ZOOM = config['CHROME_ZOOM']
    bboxes=np.load(bbox_file) # lat-lat-lon-lon format bboxes
    tiles = [[i,geo_tiles_by_bbox(b,MAP_ZOOM,IMAGE_W,IMAGE_H,CHROME_ZOOM)] for i,b in zip(range(len(bboxes)),bboxes)]
    
    tiles={'config':config, 'tiles':tiles}
    with open(targe_file,'w') as f:
        json.dump(tiles,f)
            
def craw(tile_file,config_file=None,change_driver=False):
    '''
    craw tiles from given tile file, config file (optional, which overrides the contained configs), and change_driver optional
    
    if change_driver, then a new driver is created for every bbox
    '''
    if not os.path.isabs(tile_file):
        tile_file = os.path.join(PATH, tile_file)

    with open(tile_file,'r') as f:
        all_tiles=json.load(f)
    
    config=all_tiles['config']
    all_tiles=all_tiles['tiles']
    
    if config_file is not None:
        if not config_file.lower() == 'none':
            if not os.path.isabs(config_file):
                config_file=os.path.join(PATH, config_file)
                
            # override config
            with open(config_file,'r') as f:
                config=json.load(f)
    
    print('start crawling',tile_file,config_file,change_driver)
    
    MAP_ZOOM = config['MAP_ZOOM']
    IMAGE_W = config['IMAGE_W']
    IMAGE_H = config['IMAGE_H']
    CHROME_ZOOM = config['CHROME_ZOOM']
    WINDOW_POS_X = config['WINDOW_POS_X']
    SYSTEM_DISPLAY_SCALING = config['SYSTEM_DISPLAY_SCALING']
    DELAY_SEC_BETWEEN_BBOX = config['DELAY_SEC_BETWEEN_BBOX']
    DELAY_SEC_BETWEEN_TILE = config['DELAY_SEC_BETWEEN_TILE']
    
    print('config','\n\t',config)
    
    if not change_driver:
        chrome_driver = start_chrome_driver(CHROME_ZOOM,WINDOW_POS_X)
        
    for index, tiles in all_tiles:
        print('\tbbox',index,'of',len(all_tiles),"tiles:",len(tiles['tiles_ij_latlon']))
        if change_driver:
            # launch a driver in selected zoom on selected position(screen)
            # one window per bbox
            chrome_driver = start_chrome_driver(CHROME_ZOOM,WINDOW_POS_X)
        
        time_stamp=datetime.utcnow().strftime("UTC %Y-%m-%d %H-%M")
        path = os.path.join(PATH,tile_file.split('.')[0],str(index),time_stamp)
        makesure_path(path)

        crawl_map_tiles(chrome_driver,tiles,path,SYSTEM_DISPLAY_SCALING, delay_between_tiles=DELAY_SEC_BETWEEN_TILE)
        if index < len(all_tiles)-1:
            time.sleep(DELAY_SEC_BETWEEN_BBOX) # delay between bboxes
        
        if change_driver:
            chrome_driver['driver'].quit()
            
    if not change_driver:
        chrome_driver['driver'].quit()
        
    print('finish')

import sys
if __name__ == '__main__':
    args=sys.argv
    if len(args)<=1:
        print('usage:')
        print('\t-c','TILE_JSON','<CONFIG_JSON>','<CHANGE_DRIVER in True or False>')
        print('\t\tcrawling data using generated tiles with optional override configs')
        print('\t-t','BBOX_NPY','CONFIG_JSON','TILE_JSON')
        print('\t\tgenerate tiles from list of bounding boxes (latmin-latmax-lonmin-lobmax vectors saved in npy format) and given configs')
        print('\t-d','CONFIG_JSON')
        print('\t\twrite default configs to a json file')
    elif len(args)>2:
        print(args)
        mode=args[1]
        param=args[2:]
        if mode=='-c':
            if len(param)<=2:
                craw(*param)
            elif len(param)==3:
                craw(param[0],param[1],bool(param[2]))
        elif mode=='-t':
            generate_tile_file(*param)
        elif mode=='-d':
            default_conf(*param)
    else:
        print(args)
#generate_tile_file('bbox_list_pop_20000.npy','config.json','tiles_list_pop_20000.json')