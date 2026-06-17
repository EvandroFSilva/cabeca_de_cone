package br.com.cabecadecone.deteccaodefalhas.controller;

import java.util.Base64;
import java.util.List;
import br.com.cabecadecone.deteccaodefalhas.dto.AnaliseResponse;
import br.com.cabecadecone.deteccaodefalhas.dto.PythonDetectRequest;
import br.com.cabecadecone.deteccaodefalhas.dto.PythonDetectResponse;
import br.com.cabecadecone.deteccaodefalhas.service.AnaliseService;
import br.com.cabecadecone.deteccaodefalhas.service.PythonDetectorService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/v1")
public class ParafusoController {

    private static final Logger log = LoggerFactory.getLogger(ParafusoController.class);

    private final AnaliseService service;
    private final PythonDetectorService pythonDetectorService;

    public ParafusoController(AnaliseService service, PythonDetectorService pythonDetectorService) {
        this.service = service;
        this.pythonDetectorService = pythonDetectorService;
    }

    @GetMapping("/status")
    public String status() {
        return "API DE DETECAO DE FALHAS OK";
    }

    @PostMapping(value = "/analisar", consumes = "multipart/form-data")
    public ResponseEntity<PythonDetectResponse> analisar(@RequestParam("imagem") MultipartFile imagem) {
        try {
            String base64 = Base64.getEncoder().encodeToString(imagem.getBytes());
            String mimeType = imagem.getContentType() != null ? imagem.getContentType() : "image/jpeg";
            String dataUri = "data:" + mimeType + ";base64," + base64;

            PythonDetectRequest request = new PythonDetectRequest(dataUri, "001");
            PythonDetectResponse response = pythonDetectorService.detectar(request);

            service.salvar(response);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("Erro ao analisar imagem: {}", e.getMessage(), e);
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/historico")
    public ResponseEntity<List<AnaliseResponse>> historico() {
        return ResponseEntity.ok(service.listarTodas());
    }

    @GetMapping("/python-health")
    public String pythonHealth() {
        return pythonDetectorService.health();
    }
}
