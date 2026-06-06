package br.com.cabecadecone.deteccaodefalhas.service;

import br.com.cabecadecone.deteccaodefalhas.dto.PythonDetectRequest;
import br.com.cabecadecone.deteccaodefalhas.dto.PythonDetectResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class PythonDetectorService {

    private final RestClient restClient;

    public PythonDetectorService() {
        this.restClient = RestClient.builder()
                .baseUrl("http://localhost:8089")
                .build();
    }

    public String health() {
        return restClient.get()
                .uri("/health")
                .retrieve()
                .body(String.class);
    }

    public PythonDetectResponse detectar(
            PythonDetectRequest request) {

        return restClient.post()
                .uri("/detect")
                .body(request)
                .retrieve()
                .body(PythonDetectResponse.class);
    }
}