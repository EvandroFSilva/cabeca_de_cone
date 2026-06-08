package br.com.cabecadecone.deteccaodefalhas.controller;


import br.com.cabecadecone.deteccaodefalhas.dto.AnaliseResponse;
import java.nio.file.Files;
import java.nio.file.Path;
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

    @PostMapping(
            value = "/analisar",
            consumes = "multipart/form-data"
    )
    public ResponseEntity<PythonDetectResponse> analisar(
            @RequestParam("imagem") MultipartFile imagem) {

        try {

            Path arquivoTemp =
                    Files.createTempFile(
                            "parafuso_",
                            ".jpg"
                    );

            imagem.transferTo(
                    arquivoTemp.toFile()
            );

            PythonDetectRequest request =
                    new PythonDetectRequest(
                            arquivoTemp.toString(),
                            "001"
                    );

            PythonDetectResponse response =
                    pythonDetectorService.detectar(
                            request
                    );

            Files.deleteIfExists(
                    arquivoTemp
            );

            return ResponseEntity.ok(
                    response
            );

        } catch (Exception e) {

            return ResponseEntity.internalServerError()
                    .build();
        }
    }

    @GetMapping("/python-health")
    public String pythonHealth() {
        return pythonDetectorService.health();
    }

    @GetMapping("/teste-detect")
    public PythonDetectResponse testeDetect() {

        PythonDetectRequest request =
                new PythonDetectRequest(
                        "C:/Users/Usuario/Downloads/archive/test/test_6.png",
                        "001"
                );

        return pythonDetectorService.detectar(request);
    }
}
