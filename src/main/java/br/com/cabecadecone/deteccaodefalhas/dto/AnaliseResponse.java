package br.com.cabecadecone.deteccaodefalhas.dto;

import java.time.LocalDateTime;

public record AnaliseResponse(
        Long id,
        LocalDateTime dataHora,
        Boolean hasFailure,
        String failureType,
        String predictedClass,
        Double confidence
) {
}
