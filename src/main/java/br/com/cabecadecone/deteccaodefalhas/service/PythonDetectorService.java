package br.com.cabecadecone.deteccaodefalhas.service;

import br.com.cabecadecone.deteccaodefalhas.dto.PythonDetectRequest;
import br.com.cabecadecone.deteccaodefalhas.dto.PythonDetectResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class PythonDetectorService {

    private final RestTemplate restTemplate;
    private final String pythonUrl;

    public PythonDetectorService(@Value("${python-detector.url}") String pythonUrl) {
        this.pythonUrl = pythonUrl;
        this.restTemplate = new RestTemplate();
    }

    public String health() {
        return restTemplate.getForObject(pythonUrl + "/health", String.class);
    }

    public PythonDetectResponse detectar(PythonDetectRequest request) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, String> body = Map.of(
                "image_url", request.image_url(),
                "screw_id", request.screw_id()
        );

        HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);

        return restTemplate.postForObject(pythonUrl + "/detect", entity, PythonDetectResponse.class);
    }
}