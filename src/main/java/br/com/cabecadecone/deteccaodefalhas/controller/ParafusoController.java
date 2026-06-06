package br.com.cabecadecone.deteccaodefalhas.controller;

import br.com.cabecadecone.deteccaodefalhas.dto.AnaliseResponse;
import br.com.cabecadecone.deteccaodefalhas.dto.PythonDetectRequest;
import br.com.cabecadecone.deteccaodefalhas.dto.PythonDetectResponse;
import br.com.cabecadecone.deteccaodefalhas.service.AnaliseService;
import br.com.cabecadecone.deteccaodefalhas.service.PythonDetectorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import io.swagger.v3.oas.annotations.Parameter;

@RestController
@RequestMapping("/api/v1")
public class ParafusoController {

    private final AnaliseService service;
    private final PythonDetectorService pythonDetectorService;

    public ParafusoController(AnaliseService service, PythonDetectorService pythonDetectorService) {
        this.service = service;
        this.pythonDetectorService = pythonDetectorService;
    }

    @GetMapping("/status")
    public String status(){
        return "API DE DETEÇÃO DE FALHAS OK"; }

    @PostMapping(value = "/analisar",
                 consumes = "multipart/form-data")
    public ResponseEntity<String> analisar(
            @Parameter(description = "Imagem Parafuso")
            @RequestParam("IMAGEM") MultipartFile imagem) {

        return ResponseEntity.ok(
                "Imagem recebida: " +
                        imagem.getOriginalFilename()
        );
    }

    @GetMapping("/python-health")
    public String pythonHealth() {
        return pythonDetectorService.health();
    }
}
