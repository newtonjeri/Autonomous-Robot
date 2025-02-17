---

# **Autonomous Mobile Robot - ROS 2 Simulation**  

This project provides a ROS 2-based simulation of an autonomous mobile robot in **Gazebo** with **navigation** capabilities.  

---

## **Setup Instructions**  

### **1. Build the Workspace**  
Open a terminal and navigate to the root directory of the workspace:  

```bash
cd ~/ros2_ws/Autonomous-Mobile-Robot/;
colcon build
```

---

### **2. Launch the Gazebo Simulation**  
Open a **new terminal**, navigate to the project root, and launch the simulation:  

```bash
cd ~/ros2_ws/Autonomous-Mobile-Robot/;
. install/setup.bash;
ros2 launch mobile_robot_bringup mobile_robot_sim.launch.py
```

---

### **3. Launch Navigation**  
Open **another terminal**, navigate to the root folder, and launch the navigation stack:  

```bash
cd ~/ros2_ws/Autonomous-Mobile-Robot/;
. install/setup.bash;
ros2 launch mobile_robot_bringup navigation.launch.py
```

---

## **Running the Simulation in RViz2**  

Once all components have started **without errors**, follow these steps:

1. **Set the Robot’s Initial Pose**  
   - In the **RViz2** window, click on the **"2D Pose Estimate"** button (top toolbar).  
   - Click and drag the mouse at the **robot's origin** (center of the white robot).  
   - Ensure the arrow points in the correct orientation.  

2. **Send a Navigation Goal**  
   - Click the **"2D Goal Pose"** button in RViz2.  
   - Click on the desired destination for the robot.  
   - The robot will autonomously move toward the target.  

---

## **Additional Notes**  
- Ensure ROS 2 (Humble or later) and all dependencies are properly installed.  
- If you encounter missing dependencies, install them using:  
  ```bash
  rosdep install --from-paths src --ignore-src -r -y
  ```  
- If Gazebo or RViz2 does not launch properly, try **sourcing the workspace** again:  
  ```bash
  source install/setup.bash
  ```

---