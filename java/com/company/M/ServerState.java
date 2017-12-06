package com.company.M;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by ftomo on 2017/10/27.
 */
public class ServerState {
    public enum SERVER_STATE {
        WAITING, CONNECTION
    }

    SERVER_STATE state = SERVER_STATE.WAITING;
    List<ServerStateChange> listeners = new ArrayList<>();

    public SERVER_STATE getState() {
        return state;
    }

    public void setState(SERVER_STATE state) {
        if(this.state!=state) {
            listeners.forEach(listener -> listener.serverStateChange(state));
            this.state = state;
        }
    }
    public void addListener(ServerStateChange listener){
        listeners.add(listener);
    }

    public void clearListener(){
        listeners.clear();
    }

    public interface ServerStateChange{
        public void serverStateChange(SERVER_STATE newState);
    }
}
