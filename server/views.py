# Create your views here.

import zmq

def handle_request(request):
	context = zmq.Context()
	
	vh = ""
	vh_ip = "localhost"
	vh_port = "5536"
	publisher = context.socket(zmq.PUB)
	publisher.bind('tcp://*:36883')

	subscriber = context.socket(zmq.SUB)
	subscriber.connect("tcp://%s:%s" % (vh_ip, vh_port)))
	subscriber.setsockopt(zmq.SUBSCRIBE, "r_"+vh)

	publisher.send(request)
	data = subscriber.recv()
	
	return data
