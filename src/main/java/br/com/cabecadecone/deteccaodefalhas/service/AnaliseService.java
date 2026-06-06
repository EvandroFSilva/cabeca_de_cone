package br.com.cabecadecone.deteccaodefalhas.service;

import br.com.cabecadecone.deteccaodefalhas.dto.AnaliseResponse;
import org.springframework.stereotype.Service;

@Service
public class AnaliseService {

    public AnaliseResponse analisar() {

        return new AnaliseResponse(
            "SEM_FALHA",
            98.5
        );
    }
}
