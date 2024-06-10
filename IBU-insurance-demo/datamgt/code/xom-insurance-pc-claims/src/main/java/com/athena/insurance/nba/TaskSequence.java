package com.athena.insurance.nba;

import java.util.LinkedList;

public class TaskSequence extends Action {
    private LinkedList<Assign> tasks;

    public TaskSequence() {
        this.tasks = new LinkedList<>();
    }

    public LinkedList<Assign> getTasks() {
        return tasks;
    }

    public void setTasks(LinkedList<Assign> tasks) {
        this.tasks = tasks;
    }

    public void prependTask(Assign r) {
        this.tasks.addFirst(r);
    }

    static public TaskSequence concat(Assign r, TaskSequence ts) {
        ts.prependTask(r);
        return ts;
    }

    static public TaskSequence empty() {
        return new TaskSequence();
    }

    static public Reassign newReassign(RecipientType recipient) {
        return new Reassign(recipient);
    }
    static public Reassign newReassign(RecipientType recipient, String suggestion) {
        return new Reassign(recipient, suggestion);
    }
    static public ReassignWithCallback newReassignWithCallback(int numDays, RecipientType recipient) {
        return new ReassignWithCallback(numDays, recipient);
    }
    static public ReassignWithCallback newReassignWithCallback(int numDays, RecipientType recipient, String suggestion) {
        return new ReassignWithCallback(numDays, recipient, suggestion);
    }
}
