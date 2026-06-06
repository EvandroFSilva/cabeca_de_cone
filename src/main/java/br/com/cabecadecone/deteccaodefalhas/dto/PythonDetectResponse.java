package br.com.cabecadecone.deteccaodefalhas.dto;

public record PythonDetectResponse(
        String screw_id,
        Boolean has_failure,
        Double confidence,
        String failure_type,
        String predicted_class,
        String model_path
) {
}
