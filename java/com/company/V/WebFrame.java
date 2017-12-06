package com.company.V;

import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;

import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

public class WebFrame extends JFrame {


    public static void main(String[] args) {
        new WebFrame();
    }
    public WebFrame(){
        super("web");

        URI uri = null;
        try {
            uri = new URI("http://www.google.co.jp");

            Desktop.getDesktop().browse(uri);
        } catch (URISyntaxException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }


        setSize(500,700);
        setVisible(true);
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        try {
            JEditorPane panel = new JEditorPane("https://docs.oracle.com/javase/tutorial/uiswing/components/editorpane.html");

            JScrollPane editorScrollPane = new JScrollPane(panel);
            editorScrollPane.setVerticalScrollBarPolicy(
                    JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
            editorScrollPane.setPreferredSize(new Dimension(500, 700));

            add(editorScrollPane,BorderLayout.CENTER);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
