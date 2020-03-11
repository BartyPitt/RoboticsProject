Robot Movement Overview
===============================

*"It would be good if the robot never did that again"*

*- Alattar, Ahmad*




Functional Overview
----------------------------------------


AddPosition
^^^^^^^^^^^
::

	def AddPosition(self , PositionName , PositionCordinates):
			'''A setter function that sets up the positions for the robot to travel to'''
			self.__positions__[PositionName] = PositionCordinates

The function is designed to store a coordinate in cartesian form in a private dictionary. This function originally stored the variables in the form 
of a Moveit Pose class , this was later changed , as it is very difficult to both view the values as well as made it very difficult to modify the values.
The function remained partially to interact with legacy code, and partially as it was thought that it maybe useful to add in a sanitization layer.


Cartesian Path
^^^^^^^^^^^^^^
::

	def CartesianPath(self, Endposition , StartPosition = None , max_tries = 10):
		'''Takes an Endpositions and generates and then acts on a motion plan to the Endposition using compute cartesian path. '''
		if StartPosition:
			StartPosition = self.CordinatesToPose(StartPosition)
		else:
			StartPosition = group.get_current_pose().pose
		
	    Endposition = self.CordinatesToPose(Endposition)
		
	    waypoints = []
		# start with the current pose
	    waypoints.append(StartPosition)
		
		
	    waypoints.append(Endposition)
	    for i in range(max_tries):
			(plan, fraction) = group.compute_cartesian_path (
									waypoints,   # waypoint poses
									0.01,        # eef_step
									0.0,         # jump_threshold
									True)        # avoid_collisions
			if fraction == 1:
				print("Motioned Planned Successfully")
				break
	    else:
			print("failed to run")
			return False

	    self.group.execute(plan , wait = True)
	    self.group.clear_pose_targets()
	    return True

The cartesian path is a function that takes in an Endposition for the robot to move to and uses the compute_cartesian_path() function to generate a cartesian path between the two.
During earlier phases of the project  , 


Current Order of Called Functions.::

*PLease PlAcE aN ImagE HerE*










