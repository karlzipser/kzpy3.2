if N['use SqueezeNet40_multirun!!!']:
    encoder0_pub = rospy.Publisher('encoder0',Int32MultiArray,queue_size = 10)
    encoder1_pub = rospy.Publisher('encoder1',Int32MultiArray,queue_size = 10)
    encoder2_pub = rospy.Publisher('encoder2',Int32MultiArray,queue_size = 10)

    header0_pub = rospy.Publisher('header0',Int32MultiArray,queue_size = 10)
    header1_pub = rospy.Publisher('header1',Int32MultiArray,queue_size = 10)
    header2_pub = rospy.Publisher('header2',Int32MultiArray,queue_size = 10)

    motor0_pub = rospy.Publisher('motor0',Int32MultiArray,queue_size = 10)
    motor1_pub = rospy.Publisher('motor1',Int32MultiArray,queue_size = 10)
    motor2_pub = rospy.Publisher('motor2',Int32MultiArray,queue_size = 10)


if N['use SqueezeNet40_multirun']:
    encoder0_pub.publish(data=Torch_network['encoder'][0])
    encoder1_pub.publish(data=Torch_network['encoder'][1])
    encoder2_pub.publish(data=Torch_network['encoder'][2])

    header0_pub.publish(data=Torch_network['heading'][0])
    header1_pub.publish(data=Torch_network['heading'][1])
    header2_pub.publish(data=Torch_network['heading'][2])

    motor0_pub.publish(data=Torch_network['motor'][0])
    motor1_pub.publish(data=Torch_network['motor'][1])
    motor2_pub.publish(data=Torch_network['motor'][2])