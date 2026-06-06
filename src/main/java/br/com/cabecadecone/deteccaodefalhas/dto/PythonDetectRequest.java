package br.com.cabecadecone.deteccaodefalhas.dto;

public record PythonDetectRequest(
        String image_url,
        String screw_id
) {
}
