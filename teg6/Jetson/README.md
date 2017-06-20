<h2>Installation scripts for Jetson TX1 and Jetson TK1.<h2b>

<h3>Install Caffe with Web Demo for Jetson TX1 (32bit-64bit)/Jetson TK1</h3>

<code>$ git clone https://github.com/ferhatkurt/Jetson.git</code></br>
<code>$ cd Jetson</code></br>
<code>$ chmod +x JetsonTX1_Caffe_with_Demo.sh</code></br>
<code>$ ./JetsonTX1_Caffe_with_Demo.sh</code></br>



Installation can continue more then 5 hours and sometimes you need to enter ubuntu password.

After installation open <b>a new terminal</b> and run 

<code>$ python ~/caffe/examples/web_demo/app.py -g</code></br>

Then open browser and type http://localhost
