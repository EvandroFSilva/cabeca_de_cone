package br.com.cabecadecone.deteccaodefalhas.dto;

public record AnaliseResponse(
        String resultado,
        Double confianca
) {
}
