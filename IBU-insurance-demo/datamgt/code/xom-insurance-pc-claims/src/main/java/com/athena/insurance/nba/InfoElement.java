package com.athena.insurance.nba;

public class InfoElement {


    private String path;
    private String questionId;
    private String type;         // TODO: should move to ref database

    public InfoElement() {}
    public InfoElement(String path, String questionId, String type) {
        this.path = path;
        this.questionId = questionId;
        this.type = type;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getQuestionId() {
        return questionId;
    }

    public void setQuestionId(String questionId) {
        this.questionId = questionId;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}