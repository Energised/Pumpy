package com.pumpy;

import androidx.appcompat.app.AppCompatActivity;

import androidx.appcompat.widget.Toolbar;

// bluetooth libs required
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.view.View;

import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.UUID;

public class MainActivity extends AppCompatActivity
{

    private String deviceName = null;
    private String deviceAddress;

    public static Handler handler;
    public static BluetoothSocket mmSocket;
    // 2 objects below are created later in this file
    public static ConnectedThread connectedThread;
    public static CreateConnectThread createConnectThread;

    // used by bluetooth handler to identify message status
    private final static int CONNECTING_STATUS = 1;
    // used by bluetooth handler to identify message update
    private final static int MESSAGE_READ = 2;
    // required tag
    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // init UI
        final Button buttonConnect = findViewById(R.id.buttonConnect);
        final Toolbar toolbar = findViewById(R.id.toolbar);

        final ProgressBar progressBar = findViewById(R.id.progressBar);
        progressBar.setVisibility(View.GONE);

        final TextView textViewInfo = findViewById(R.id.textViewInfo);
        final Button buttonActivate = findViewById(R.id.buttonActivate);

        // setup input boxes
        final Spinner sizeSpinner = (Spinner) findViewById(R.id.sizeSpinner);
        // create ArrayAdapter for spinner
        ArrayAdapter<CharSequence> sizeAdapter = ArrayAdapter.createFromResource(this,
                R.array.size_list, android.R.layout.simple_spinner_item);
        sizeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        sizeSpinner.setAdapter(sizeAdapter);

        final EditText timeInput = (EditText) findViewById(R.id.timeNumber);

        final Spinner msSpinner = (Spinner) findViewById(R.id.msSpinner);
        ArrayAdapter<CharSequence> msAdapter = ArrayAdapter.createFromResource(this,
                R.array.ms_list, android.R.layout.simple_spinner_item);
        msAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        msSpinner.setAdapter(msAdapter);

        // check if bluetooth device has already been selected via SelectDeviceActivity
        deviceName = getIntent().getStringExtra("deviceName");
        if(deviceName != null)
        {
            // device exists, get info to make connection
            deviceAddress = getIntent().getStringExtra("deviceAddress");
            toolbar.setSubtitle("Connecting to: " + deviceName);
            progressBar.setVisibility(View.VISIBLE);
            buttonConnect.setEnabled(false);

            // call a new thread to create bluetooth connection to the deviceName recieved
            BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
            createConnectThread = new CreateConnectThread(bluetoothAdapter, deviceAddress);
            createConnectThread.start();
        }

        // gui handler
        handler = new Handler(Looper.getMainLooper())
        {
            @Override
            public void handleMessage(Message msg)
            {
                switch(msg.what)
                {
                    case CONNECTING_STATUS:
                        switch(msg.arg1)
                        {
                            case 1:
                                toolbar.setSubtitle("Connected to: " + deviceName);
                                progressBar.setVisibility(View.GONE);
                                buttonConnect.setEnabled(true);
                                break;
                            case -1:
                                toolbar.setSubtitle("Failed to connect");
                                progressBar.setVisibility(View.GONE);
                                buttonConnect.setEnabled(true);
                                break;
                        }
                        break;
                    case MESSAGE_READ:
                        // message received from pi
                        String piMsg = msg.obj.toString();
                        textViewInfo.setText(piMsg);
                        break;
                }
            }
        };

        buttonConnect.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                // when connect button pressed, start SelectDeviceActivity
                Intent intent = new Intent(MainActivity.this, SelectDeviceActivity.class);
                startActivity(intent);
            }
        });

        buttonActivate.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                // setup data to be sent to Pi
                String size = sizeSpinner.getSelectedItem().toString();
                String time = timeInput.getText().toString();
                String ms = msSpinner.getSelectedItem().toString();
                String data = size + "," + time + "," + ms;
                connectedThread.write(data);
            }
        });
    }

    // now define classes for ConnectedThread and CreateConnectedThread

    public static class CreateConnectThread extends Thread
    {
        public CreateConnectThread(BluetoothAdapter bluetoothAdapter, String address)
        {
            // use a temporary BluetoothSocket until assigned to the main program
            BluetoothDevice bluetoothDevice = bluetoothAdapter.getRemoteDevice(address);
            BluetoothSocket tmp = null;
            // UUID uuid = bluetoothDevice.getUuids()[0].getUuid();
            // this UUID below works with wanspiron laptop
            // UUID uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
            // now trying a UUID for generic access from the RPi itself (didnt work)
            // UUID uuid = UUID.fromString("00001801-0000-1000-8000-00805F9B34FB");
            // trying new UUID from supposedly working app on github
            UUID uuid = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee");

            try
            {
                // get a BluetoothSocket to connect with the given BluetoothDevice
                // NOTE: android device varieties means we may have to try other methods
                // tmp = bluetoothDevice.createRfcommSocketToServiceRecord(uuid);
                tmp = bluetoothDevice.createInsecureRfcommSocketToServiceRecord(uuid);
            }
            catch(IOException e)
            {
                Log.e(TAG, "Sockets create() method failed", e);
            }
            mmSocket = tmp;
        }

        public void run()
        {
            // now we have the connection to the device, cancel discovery
            // otherwise it can slow down the connection
            BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
            bluetoothAdapter.cancelDiscovery();

            try
            {
                // connect to remote device through socket
                // handler blocks actions until it succeeds or throws an exception
                mmSocket.connect();
                Log.e("Status", "Device connected");
                handler.obtainMessage(CONNECTING_STATUS, 1, -1).sendToTarget();
            }
            catch(IOException connectException)
            {
                // unable to connect, close socket and return
                try
                {
                    mmSocket.close();
                    Log.e("Status", "Cannot connect to device");
                    handler.obtainMessage(CONNECTING_STATUS, -1, -1).sendToTarget();
                }
                catch(IOException closeException)
                {
                    Log.e(TAG, "Could not close the client socket", closeException);
                }
                return;
            }

            // connection attempt succeeded
            // perform work associated with connection in separate thread
            connectedThread = new ConnectedThread(mmSocket);
            connectedThread.run();
        }

        //
        public void cancel()
        {
            try
            {
                mmSocket.close();
            }
            catch(IOException e)
            {
                Log.e(TAG, "Could not close the client socket", e);
            }
        }
    }

    // thread for data transfer
    public static class ConnectedThread extends Thread
    {
        private final BluetoothSocket mmSocket;
        private final InputStream mmInStream;
        private final OutputStream mmOutStream;

        public ConnectedThread(BluetoothSocket socket)
        {
            mmSocket = socket;
            InputStream tmpIn = null;
            OutputStream tmpOut = null;

            // get input/output stream using temp objects
            // member streams are final
            try
            {
                tmpIn = socket.getInputStream();
                tmpOut = socket.getOutputStream();
            }
            catch(IOException e)
            {
                // just catch it for now
            }

            mmInStream = tmpIn;
            mmOutStream = tmpOut;
        }

        public void run()
        {
            byte[] buffer = new byte[1024]; // buffer store for the stream
            int bytes = 0; // bytes returned from read()
            // keep listening to the InputStream until an exception occurs
            while(true)
            {
                try
                {
                    // read from InputStream until termination character is received
                    // then sends the whole string to the GUI handler
                    buffer[bytes] = (byte) mmInStream.read();
                    String readMessage;
                    if(buffer[bytes] == '\n')
                    {
                        readMessage = new String(buffer, 0, bytes);
                        Log.e("Recieved Message", readMessage);
                        handler.obtainMessage(MESSAGE_READ, readMessage).sendToTarget();
                        bytes = 0;
                    }
                    else
                    {
                        bytes++;
                    }
                }
                catch(IOException e)
                {
                    e.printStackTrace();
                    break;
                }
            }
        }

        // call this from MainActivity to send data to the remote device
        public void write(String input)
        {
            byte[] bytes = input.getBytes();
            try
            {
                mmOutStream.write(bytes);
            }
            catch(IOException e)
            {
                Log.e("Send error", "Unable to send message", e);
            }
        }

        public void cancel()
        {
            try
            {
                mmSocket.close();
            }
            catch(IOException e)
            {
                // do something here later
            }
        }
    }

    // terminate connection onBackPressed
    @Override
    public void onBackPressed()
    {
        // terminate bluetooth connection and close app
        if(createConnectThread != null)
        {
            createConnectThread.cancel();
        }
        Intent a = new Intent(Intent.ACTION_MAIN);
        a.addCategory(Intent.CATEGORY_HOME);
        a.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(a);
    }
}