package com.company.M;

import com.company.V.MainFrame;

import java.awt.*;
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.ConcurrentLinkedQueue;
import static com.company.M.ServerState.SERVER_STATE;

import javax.sound.sampled.*;

public class Server implements Runnable {



    private enum EVENT {
        START_WAIT,START_MAIN
    }



    Queue<EVENT> events = new ConcurrentLinkedQueue<>(); //thread safe queue
    ServerSocket serverSocket;

    Socket socket;

    private Object ACCESS_PORT_MUTEX = new Object();
    private int acceptPort = 50001;


    public static final int LIMIT_TIME = 60; //seconds
    
    private String webPageName = "80001/??.php";

    private String saveFile = "option.properties";

    private String MESSAGE_START ="0";
    private String MESSAGE_STOP ="1";
    ServerState server_state = new ServerState();
    MainFrame mainFrame;

    private long targetMillis = -1;
    public Server(MainFrame mainFrame) {
        this.mainFrame =mainFrame;


        try {
            File f = new File(saveFile);
            if(f.exists()){
                Properties prop =  new Properties();
                prop.load(new FileInputStream(f));
                for (Map.Entry<Object,Object> entry : prop.entrySet()) {
                    switch (String.valueOf(entry.getKey())){
                        case "acceptPort":
                            acceptPort = Integer.valueOf(String.valueOf(entry.getValue()));
                            break;
                        case "webPageName":
                            webPageName = String.valueOf(entry.getValue());
                            break;
                    }
                }
            }
        }catch (IOException e){
            e.printStackTrace();
        }



        this.settingUpdate();
        server_state.addListener(new ServerState.ServerStateChange() {
            @Override
            public void serverStateChange(SERVER_STATE newState) {
                // initialize

                mainFrame.setServerState(newState);
                if (newState == SERVER_STATE.WAITING){
                    targetMillis = -1;
                    socket=null;
                }
                if(newState == SERVER_STATE.CONNECTION){
                    mainFrame.setIPAddress(socket.getInetAddress());
                }

            }
        });
    }


    public void run() {
        EVENT event;
        while (true){
            while((event=events.poll())!=null){
                if(event==EVENT.START_WAIT){
                    if(server_state.getState()!=SERVER_STATE.WAITING) throw new IllegalStateException();
                        if(!serverSocket.isClosed()){
                            try {
                                System.out.println("Accepting ....");
                                mainFrame.setAccepting();
                                socket = serverSocket.accept();
                                System.out.println("Connection "+socket.getInetAddress());
                                server_state.setState(SERVER_STATE.CONNECTION);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                }else if(event == EVENT.START_MAIN) {
                    if (server_state.getState() != SERVER_STATE.CONNECTION) throw new IllegalStateException();
                    mainFrame.setCounting(true);
                    if (socket == null) throw new NullPointerException("client socket is null ");
                    try {
                        System.out.println(MESSAGE_START);
                        sendMessage(MESSAGE_START);
                        System.out.println("Send");
                    } catch (IOException e) {
                        if (e instanceof SocketException) {
                            server_state.setState(SERVER_STATE.WAITING);
                        }
                        e.printStackTrace();
                    }
                }
            }
            if(server_state.getState() == SERVER_STATE.CONNECTION &&
                    targetMillis >0){
                int sa = (int)((targetMillis-System.currentTimeMillis())/1000);
                mainFrame.updateTime(sa);
                if(sa==0){
                    try {

                        playSound();
                        this.sendMessage(MESSAGE_STOP);
                        showBrowser();
                        mainFrame.setCounting(false);
                        this.targetMillis=-1;
                    }catch (IOException e) {
                        if(e instanceof SocketException){
                            server_state.setState(SERVER_STATE.WAITING);
                        }
                        e.printStackTrace();
                    }

                }

            }

        }
    }

    private void showBrowser() {
        try {
            Thread.sleep(1000   );
            URI uri = new URI("http://" + socket.getInetAddress().toString().substring(1) + ":"+webPageName);
            Desktop.getDesktop().browse(uri);
        }catch (URISyntaxException | IOException e){
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private void sendMessage(final String SEND_MESSAGE) throws IOException{
        BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        PrintWriter writer = new PrintWriter(socket.getOutputStream(),true);
        String message = null;
        do{
            writer.print(SEND_MESSAGE +"\n");
            writer.flush();
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("ready  :"+reader.ready());

            if(reader.ready()) {
                message = reader.readLine();
                System.out.println("recieve :"+message);
            }
        }while (message==null || !message.equals("0"));
        System.out.println("sending Message : "+SEND_MESSAGE);
        targetMillis = System.currentTimeMillis()+LIMIT_TIME*1000;


    }

    public void settingUpdate(){
        if(server_state.getState()==SERVER_STATE.CONNECTION){
            try {
                serverSocket.close();
            }catch (IOException io){
                io.printStackTrace();
            }
            server_state.setState(SERVER_STATE.WAITING);
        }

        try {

            synchronized (ACCESS_PORT_MUTEX) {
                if(serverSocket != null){
                    serverSocket.close();
                }
                serverSocket = new ServerSocket(acceptPort);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }


        //----saving-------
        Map<String,String> data  = new HashMap<String,String >(){{
            put("acceptPort",String.valueOf(acceptPort));
            put("webPageName",webPageName);
        }};

        Properties prop = new Properties();
        prop.putAll(data);
        File f = new File(saveFile);
        try {
            if (!f.exists()) {
                f.createNewFile();
            }
            prop.store(new FileOutputStream(f), null);


        }catch (IOException e){
            e.printStackTrace();
        }
    }
    public void startWaiting(){
        events.add(EVENT.START_WAIT);
    }

    public void startMain(){
        events.add(EVENT.START_MAIN);
    }




    public int getAcceptPort() {
        int temp;
        synchronized (ACCESS_PORT_MUTEX){
            temp = acceptPort;
        }
        return temp;
    }

    public void setAcceptPort(int port){
        synchronized (ACCESS_PORT_MUTEX) {
            acceptPort = port;
        }
    }

    public String getWebPageName() {
        return webPageName;
    }

    public void setWebPageName(String webPageName) {
        this.webPageName = webPageName;
    }

    private void playSound(){

        final AudioInputStream ais;
        try {
            ais = AudioSystem.getAudioInputStream(new File("Sound.wav"));
            ais.getFormat();
            final Clip line = AudioSystem.getClip();
            line.open(ais);
            line.start();
            Thread.sleep(1);
            line.drain();
            line.stop();
            line.close();
        } catch (UnsupportedAudioFileException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (LineUnavailableException e) {
            e.printStackTrace();
        }

    }

}

