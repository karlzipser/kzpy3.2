'''
Created on Apr 12, 2017

@author: Sascha Hornauer
'''
import numpy as np
import sys
import os
import cv2
import random
from aruco_tools.Marker import Marker
from data_parsing.Bagfile_Handler import Bagfile_Handler
import aruco_tools.aruco_angle_retriever as aruco_data

    
class Top_View(object):
    
    persistent_markers = {}
    base_marker = None
    frame_number = 0
        
    def __init__(self):
        pass      

    
    
    def show_top_view(self, input_markers):
       
        cv_image = np.ones((600, 600, 3), np.uint8)
        
        # Some arbitrary scaling parameters for visualisation are set
        scale_factor = int(100.0 * (1.0 / 8.0))
        shift_factor = 300
        turn_factor = np.pi / 2.0 
        
        current_visible_markers = {}
        
        
        # Reduce confidence for each marker in the persistent list, if there are any yet
#         for marker_id in self.persistent_markers:
#             self.persistent_markers[marker_id].confidence = self.persistent_markers[marker_id].confidence - 0.1
        # Replace that concept with a more complete notion about the confidence
        
        # Add markers to list, overwriting old markers and thereby recalculating confidence levels
        for marker in input_markers:
            # If the marker is already in the persistent list
            # update some fields, and leave others as the shift information untouched
            if marker.marker_id in self.persistent_markers.keys():
                known_marker = self.persistent_markers[marker.marker_id]
                known_marker.update_perception(marker.corners_xy, marker.rvec, marker.tvec)
                current_visible_markers[marker.marker_id] = known_marker                
            else:   
                self.persistent_markers[marker.marker_id] = marker
                current_visible_markers[marker.marker_id] = marker
            
        # See if the initial marker is found, if not take the first of the visible ones
        if self.base_marker == None:
            # first entry is used
            self.base_marker = current_visible_markers.itervalues().next()            
            orig_xy, orig_distance, orig_angle = self.get_marker_xy(self.base_marker)
            self.base_marker.update_pos_and_shift(orig_xy, orig_distance, (0.0, (0.0, 0.0)))
        
        for current_marker in current_visible_markers.values():
            # Go over all visible marker to calculate their rotation and translation relative 
            # to the base marker
            
            # If we are looking at the base marker, we just update its position. It has no shift
            if current_marker == self.base_marker:
                orig_xy, orig_distance, orig_angle = self.get_marker_xy(current_marker)
                self.base_marker.update_pos_and_shift(orig_xy, orig_distance, (0.0, (0.0, 0.0)))
        
            # If we dont look at the base marker though it was found beforehand
            else:                
                # we check if the base marker is still visible
                if self.base_marker.marker_id in current_visible_markers:
                    
                    # do shift calculations according to base marker and write them to the current marker
                    self.update_pos_shift_to_base(self.base_marker, current_marker)                    
                    # self.persistent_markers[current_marker.marker_id] = current_marker  
                    self.persistent_markers[current_marker.marker_id] = current_marker
                    
                    
                else:
                    # The base marker is no longer visible
                    # Update the pos based on the saved shift values
                    # In the future check distance stuff
                    if current_marker.shift_angle_trans != None:
                        self.update_pos_given_shift(current_marker)
                        self.persistent_markers[current_marker.marker_id] = current_marker
                    else:    
                        # If there are no such information we see a new marker and have to infer
                        # shift over an intermediate marker
                        #
                        # For each marker in the visible markers list we look for one with existing shift values
                        # to calculate everything in respect to this one
                        intermediate_marker = None
                        for tmp_marker in current_visible_markers.values():
                            if tmp_marker.marker_id != current_marker.marker_id and tmp_marker.shift_angle_trans != None:
                                # If we found a different marker with shift values we have found an intermediate
                                intermediate_marker = tmp_marker
                            elif tmp_marker.shift_angle_trans == None:
                                # If we found a marker without those values we need to look further
                                print("Marker " + str(tmp_marker.marker_id) + " Has no shift values")
                                continue
                            elif len(current_visible_markers) < 2:
                                # If the current marker id is the same as the only one left in the list, 
                                # and this only marker has no shift information, we dont know our position
                                    print("Warning, no more markers with knowledge about the base found")
                            
                        if(intermediate_marker == None):
                            print("Warning, no intermediate marker found")
                        else:                      
                            print("Found intermediate marker " + str(intermediate_marker.marker_id) + " for " + str(current_marker.marker_id))
                            self.calculate_marker_to_inter(intermediate_marker, current_marker)
                            self.persistent_markers[current_marker.marker_id] = current_marker
                          
        # self.persistent_markers.update(current_visible_markers)

        for marker in self.persistent_markers.values():
            try:
                
                pos_x = marker.pos_xy[0]
                pos_y = marker.pos_xy[1]
                confidence_level = marker.confidence
                # confidence_level = 1.0
                cv2.circle(cv_image, (int(scale_factor * pos_x) + shift_factor, int(scale_factor * pos_y) + shift_factor), 2, (255 * confidence_level, 0, 0), 2)
            except AttributeError as ex:
                print(str(ex) + str(marker.marker_id))
                pass
            except TypeError as ex:
                print(ex)
                pass

        cv2.imshow('topView', cv_image)
        cv2.moveWindow('topView', 700, 0)

    def get_marker_xy(self, marker):
        distance = aruco_data.get_distance(marker)
        angle = aruco_data.get_angle_surface(marker)
        # angle = aruco_data.get_angle_to_center(marker)
        # Now we can get the dx and dy of movement
        xy = cv2.polarToCart(distance, angle)
        return tuple((xy[0][0][0], xy[1][0][0])), distance, angle
    
    def update_pos_shift_to_base(self, base_marker, marker_b):
        
        # Get the data of the new perceived marker
        position_current_xy, distance_current, angle_surface_current = self.get_marker_xy(marker_b)
        
        # Get the data of the base marker, perceived from the new position
        base_xy, dist_base, ang_base = self.get_marker_xy(base_marker)
         
        # Calculate the difference in angle for coordination transform rotation
        phi = ang_base - angle_surface_current
        
        # Calculate the translation by calculating the coordinates according to the rotated origin
        trans_pos_xy = cv2.polarToCart(distance_current, phi)
        trans_pos_xy = (trans_pos_xy[0][0][0], trans_pos_xy[1][0][0])
        
        # The translation vector is now the difference between the coordinates, relative to
        # the base marker and the coordinates, relative to the new marker
        trans_rel_base = np.subtract(base_xy, trans_pos_xy)                  
         
        # Our position in the system of the base marker, given by the new marker, can now be calculated
        # First the rotation is applied
        new_x = position_current_xy[0] * np.cos(phi) + position_current_xy[1] * np.sin(phi)
        new_y = position_current_xy[0] * np.sin(phi) + position_current_xy[1] * np.cos(phi)
         
        # Then the translation is performed                                       
        resulting_x = new_x + trans_rel_base[0]
        resulting_y = new_y + trans_rel_base[1]
        
        # Write the resulting data into the marker
        marker_b.update_pos_and_shift((resulting_x, resulting_y),distance_current,(phi, (trans_rel_base)))

        
    def update_pos_given_shift(self, single_marker):
        # Get the data of the new perceived marker
        position_current_xy, distance_current, angle_surface_current = self.get_marker_xy(single_marker)
         
        # Calculate the difference in angle for coordination transform rotation
        phi = single_marker.shift_angle_trans[0]
        
        # Calculate the translation by calculating the coordinates according to the rotated origin
        trans_pos_xy = cv2.polarToCart(distance_current, phi)
        trans_pos_xy = (trans_pos_xy[0][0][0], trans_pos_xy[1][0][0])
        
        # The translation vector is now the difference between the coordinates, relative to
        # the base marker and the coordinates, relative to the new marker
        trans_rel_base = single_marker.shift_angle_trans[1]             
         
        # Our position in the system of the base marker, given by the new marker, can now be calculated
        # First the rotation is applied
        new_x = position_current_xy[0] * np.cos(phi) + position_current_xy[1] * np.sin(phi)
        new_y = position_current_xy[0] * np.sin(phi) + position_current_xy[1] * np.cos(phi)
         
        # Then the translation is performed                                       
        resulting_x = new_x + trans_rel_base[0]
        resulting_y = new_y + trans_rel_base[1]
        
        # Write the resulting data into the marker
        single_marker.update_pos_and_shift((resulting_x, resulting_y),distance_current,(phi, (trans_rel_base)))

        
        
    def calculate_marker_to_inter(self, interim_marker, marker_b):

        
        # Get the data of the new perceived marker
        position_current_xy, distance_current, angle_surface_current = self.get_marker_xy(marker_b)
        
        # Get the data of the interim marker, perceived from the new position
        interim_xy, dist_interim, ang_interim = self.get_marker_xy(interim_marker)
         
        # Calculate the difference in angle for coordination transform rotation
        phi_marker_to_interim = ang_interim - angle_surface_current
         
        # Calculate the translation by calculating the coordinates according to the rotated origin
        trans_pos_xy = cv2.polarToCart(distance_current, phi_marker_to_interim)
        trans_pos_xy = (trans_pos_xy[0][0][0], trans_pos_xy[1][0][0])
        
        # The translation vector is now the difference between the coordinates, relative to
        # the interim marker and the coordinates, relative to the new marker
        trans_rel_interim = np.subtract(interim_xy, trans_pos_xy)                  
         
        # Our position in the system of the interim marker, given by the new marker, can now be calculated
        # First the rotation is applied
        new_x = position_current_xy[0] * np.cos(phi_marker_to_interim) + position_current_xy[1] * np.sin(phi_marker_to_interim)
        new_y = position_current_xy[0] * np.sin(phi_marker_to_interim) + position_current_xy[1] * np.cos(phi_marker_to_interim)
         
        # Then the translation is performed                                       
        resulting_x = new_x + trans_rel_interim[0]
        resulting_y = new_y + trans_rel_interim[1]
        
        # Now the shift needs to be done again to the base system. 
        # The shift values from the intermediate marker are known
        # Calculate the difference in angle for coordination transform rotation
        phi_interim_to_base = interim_marker.shift_angle_trans[0]
        
        # Calculate the translation by calculating the coordinates according to the rotated origin
        trans_pos_xy = cv2.polarToCart(dist_interim, phi_interim_to_base)
        trans_pos_xy = (trans_pos_xy[0][0][0], trans_pos_xy[1][0][0])
        
        # The translation vector is also in the marker 
        trans_rel_base = interim_marker.shift_angle_trans[1]             
         
        # Our position in the system of the base marker, given by the new marker, can now be calculated
        # First the rotation is applied
        new_x = resulting_x * np.cos(phi_interim_to_base) + resulting_x * np.sin(phi_interim_to_base)
        new_y = resulting_y * np.sin(phi_interim_to_base) + resulting_y * np.cos(phi_interim_to_base)
         
        # Then the translation is performed                                       
        resulting_x = new_x + trans_rel_base[0]
        resulting_y = new_y + trans_rel_base[1]
        
        # Write the resulting data into the marker
        marker_b.update_pos_and_shift((resulting_x, resulting_y), distance_current, (phi_interim_to_base - phi_marker_to_interim, (trans_rel_base + trans_rel_interim)))
        

if __name__ == "__main__":
    visualizer = Top_View()
    bagfile_path = sys.argv[1]
    
    bagfile_handler = Bagfile_Handler(bagfile_path)
    paused_video = False
    
    head, tail = os.path.split(bagfile_path)
    
    while(True):
        if not paused_video:
            cv_image = bagfile_handler.get_image()
        
            markers = aruco_data.get_markers_in_image(cv_image)
            visualizer.show_top_view(markers)
            # visualizer.visualize_markers_center_line(markers,tail,cv_image)
        cv2.imshow("video", cv_image)
        
        key = cv2.waitKey(1000 / 30) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):
            paused_video = not paused_video
        if key == ord('w'):
            bagfile_handler.fast_forward()
            
            
#             
#             # Get the data of the new perceived marker
#                     position_current_xy, distance_current, angle_surface_current = self.get_marker_xy(current_marker)
#                     
#                     # Check if that marker already has shift values
#                     if(current_marker.marker_id in self.marker_positions and self.marker_positions[current_marker.marker_id].get_shift_ang_trans() != None):
#                         # If that is the case only the position is updated
#                         self.marker_positions[current_marker.marker_id].set_pos_xy(position_current_xy)
#                         continue
#                      
#                       
#                     # Get the data of the intermediate marker, perceived from the new position
#                     interim_marker_pos = self.marker_positions.values()[0]
#                     pos_interim_xy, dist_interim, ang_interim = self.get_marker_xy(self.persistent_markers[str(interim_marker_pos.get_marker_id())])
#                     
#                     # Get its shift phi and translation  
#                     phi_to_base = interim_marker_pos.get_shift_ang_trans()[0]
#                     trans_to_base = interim_marker_pos.get_shift_ang_trans()[1]
#                     
#                     # Calculate the angle shift in between the two markers and in between the marker and the base  
#                     # known from the interim marker to have the overall shift
#                     phi = ang_interim - angle_surface_current - phi_to_base
#                       
#                     # Calculate the translation to the interim vector, by first turning appropriately
#                     trans_pos_xy = cv2.polarToCart(distance_current, ang_interim - angle_surface_current)
#                     trans_pos_xy = (trans_pos_xy[0][0][0],trans_pos_xy[1][0][0])  
#                     
#                     trans_to_interim = np.subtract(pos_interim_xy, trans_pos_xy)
#                     # The translation vector is now the difference between the translation to the
#                     # base marker and the translation to the interim marker
#                     # trans to base is already base_xy - interim_xy
#                     trans_rel_base = np.subtract(trans_to_base, trans_to_interim)     
#                     
#                     # Our position in the system of the base marker, given by the new marker, can now be calculated
#                     # First the rotation is applied by the whole phi angle
#                     new_x = position_current_xy[0] * np.cos(phi) + position_current_xy[1] * np.sin(phi)
#                     new_y = position_current_xy[0] * np.sin(phi) + position_current_xy[1] * np.cos(phi)
#                      
#                     # Then the translation is performed by the whole translation vector                                
#                     resulting_x = new_x + trans_rel_base[0]
#                     resulting_y = new_y + trans_rel_base[1]
#                      
#                     # The position is written into a marker position, which is technically our position perceived under the
#                     # new marker, transformed into the reference frame of the base marker
#                     new_marker_position = Marker_Position(current_marker.marker_id, (resulting_x, resulting_y), (phi, (trans_rel_base)), distance_current)
#                       
