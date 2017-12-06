package com.company.V;


import com.company.M.Server;
import com.company.M.ServerState;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.InetAddress;

public class MainFrame extends JFrame{
    public static final Font font = new Font("ＭＳ ゴシック", Font.PLAIN, 30);
    public static final Font font_medium = new Font("ＭＳ ゴシック", Font.PLAIN, 80);
    public static final Font font_large = new Font("ＭＳ ゴシック", Font.PLAIN, 330);

    private boolean isWaitingMode = true;

    Server server;

    public static void main(String[] args) {
        new MainFrame().setVisible(true);
    }

    public MainFrame() {
        super("ShutterChance!");
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        setSize(800,600);
        setJMenuBar(createMenuBar());

        server = new Server(this);

        setWaitPanels();

        Thread ses = new Thread(server);
        ses.start();
        //setMainPanels();
        waitingButton.doClick();
    }


    private JMenuBar createMenuBar(){
        JMenuBar menuBar = new JMenuBar();
        JButton optionButton = new JButton("option");
        menuBar.add(optionButton);
        optionButton.setFont(font);
        optionButton.addActionListener((ActionEvent e) -> {
            settingFrame frame = new settingFrame(server);
            frame.pack();
            frame.setVisible(true);


        });
        return menuBar;
    }

    JButton waitingButton;
    private void setWaitPanels() {
        waitingButton = new JButton("接続待ち開始");
        waitingButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                ((JButton) e.getSource()).setEnabled(false);
                server.startWaiting();
            }
        });
        waitingButton.setFont(MainFrame.font_medium);
        getContentPane().removeAll();
        getContentPane().add(waitingButton, BorderLayout.CENTER);

        timeLabel=null;
        playButton = null;
    }
    JLabel timeLabel;
    JLabel ipLabel;
    JButton playButton;
    private void setMainPanels(){
        ipLabel = new JLabel();
        ipLabel.setFont(font_medium);
        ipLabel.setHorizontalAlignment(JLabel.CENTER);


        timeLabel = new JLabel(Server.LIMIT_TIME+"");
        timeLabel.setFont(font_large);
        timeLabel.setHorizontalAlignment(JLabel.CENTER);

        JPanel labelPanel = new JPanel();
        JPanel labelPanel2 = new JPanel();

        labelPanel.setLayout(new GridLayout(1,1));
        labelPanel.setBorder(new EmptyBorder(50,50,50,50));
        labelPanel.add(labelPanel2);

        labelPanel2.setBorder(new LineBorder(Color.BLACK,3));
        labelPanel2.setLayout(new GridLayout(1,1));
        labelPanel2.add(timeLabel);

        playButton = new JButton("Play");
        playButton.setFont(font);
        playButton.addActionListener(e -> server.startMain());
        playButton.setBorder(new LineBorder(Color.BLACK,1));
        playButton.setPreferredSize(new Dimension(700,60));
        JPanel buttonPanel = new JPanel();
        buttonPanel.setPreferredSize(new Dimension(800,100));
        buttonPanel.add(playButton);
        getContentPane().removeAll();

        getContentPane().add(ipLabel,BorderLayout.PAGE_START);
        getContentPane().add(labelPanel,BorderLayout.CENTER);
        getContentPane().add(buttonPanel,BorderLayout.PAGE_END);
    }


    public void setServerState(ServerState.SERVER_STATE serverState){
        if(serverState == ServerState.SERVER_STATE.WAITING){
            setWaitPanels();
        }else{
            setMainPanels();
        }
        getContentPane().validate();
    }

    public void updateTime(int leftMinute){
        if(timeLabel==null) throw new IllegalStateException();
        if(leftMinute <= 5){
            timeLabel.setForeground(Color.RED);
        }else{
            timeLabel.setForeground(Color.black);
        }

        timeLabel.setText(""+leftMinute);
    }


    public void setCounting(boolean b) {
        if(playButton==null) throw new NullPointerException("playButton is null");
        playButton.setEnabled(!b);
    }

    public void setAccepting(){
        waitingButton.setText("Waiting...");
    }

    public void setIPAddress(InetAddress address){
        this.ipLabel.setText(address.toString().substring(1));
    }
}
