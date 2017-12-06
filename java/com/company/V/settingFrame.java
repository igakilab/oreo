package com.company.V;

import com.company.M.Server;

import javax.swing.*;
import javax.swing.text.*;
import java.awt.*;
import java.awt.event.*;

public class settingFrame extends JDialog {
    private JPanel contentPane;
    private JButton buttonOK;
    private JButton buttonCancel;
    private JTextField acceptPort;
    private JLabel acceptPortLabel;
    private JLabel webPageNameLabel;
    private JTextField webPageName;
    private Server server;

    public settingFrame(Server server) {
        setContentPane(contentPane);
        setModal(true);
        this.server = server;
        getRootPane().setDefaultButton(buttonOK);

        buttonOK.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                onOK();
            }
        });
        buttonOK.setFont(MainFrame.font);

        buttonCancel.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                onCancel();
            }
        });

        webPageName.setText(server.getWebPageName());
        acceptPort.setText(String.valueOf(server.getAcceptPort()));
        PlainDocument doc = ((PlainDocument) acceptPort.getDocument());

        acceptPort.addKeyListener(new KeyAdapter() {
            public void keyTyped(KeyEvent e) {
                char c = e.getKeyChar();
                if (!((c >= '0') && (c <= '9') ||
                        (c == KeyEvent.VK_BACK_SPACE) ||
                        (c == KeyEvent.VK_DELETE))) {
                    e.consume();
                }
            }
        });


        buttonCancel.setFont(MainFrame.font);
     //   acceptPortLabel.setFont(MainFrame.font_medium);
       // webPageNameLabel.setFont(MainFrame.font_medium);
        // call onCancel() when cross is clicked
        setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                onCancel();
            }
        });

        // call onCancel() on ESCAPE
        contentPane.registerKeyboardAction(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                onCancel();
            }
        }, KeyStroke.getKeyStroke(KeyEvent.VK_ESCAPE, 0), JComponent.WHEN_ANCESTOR_OF_FOCUSED_COMPONENT);
    }





    private void onOK() {
        String portStr = acceptPort.getText();
        int port = Integer.parseInt(acceptPort.getText());
        server.setAcceptPort(port);
        server.setWebPageName(webPageName.getText());
        server.settingUpdate();

        dispose();
    }

    private void onCancel() {
        // add your code here if necessary
        dispose();
    }


    private void createUIComponents() {
        acceptPortLabel = new JLabel();
        acceptPortLabel.setFont(MainFrame.font);
        webPageNameLabel=new JLabel();
        webPageNameLabel.setFont(MainFrame.font);
        webPageName=new JTextField();
        webPageName.setFont(MainFrame.font);
        webPageName.setMinimumSize(new Dimension(500,0));
        acceptPort = new JTextField();
        acceptPort.setFont(MainFrame.font);



    }
}
