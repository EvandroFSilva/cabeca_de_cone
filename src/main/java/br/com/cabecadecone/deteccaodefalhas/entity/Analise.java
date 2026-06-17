package br.com.cabecadecone.deteccaodefalhas.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "analises")
public class Analise {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private LocalDateTime dataHora;
    private Boolean hasFailure;
    private String failureType;
    private String predictedClass;
    private Double confidence;

    public Long getId() { return id; }
    public LocalDateTime getDataHora() { return dataHora; }
    public Boolean getHasFailure() { return hasFailure; }
    public String getFailureType() { return failureType; }
    public String getPredictedClass() { return predictedClass; }
    public Double getConfidence() { return confidence; }

    public void setDataHora(LocalDateTime dataHora) { this.dataHora = dataHora; }
    public void setHasFailure(Boolean hasFailure) { this.hasFailure = hasFailure; }
    public void setFailureType(String failureType) { this.failureType = failureType; }
    public void setPredictedClass(String predictedClass) { this.predictedClass = predictedClass; }
    public void setConfidence(Double confidence) { this.confidence = confidence; }
}
