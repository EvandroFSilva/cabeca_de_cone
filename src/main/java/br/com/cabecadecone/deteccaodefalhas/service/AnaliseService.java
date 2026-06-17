package br.com.cabecadecone.deteccaodefalhas.service;

import br.com.cabecadecone.deteccaodefalhas.dto.AnaliseResponse;
import br.com.cabecadecone.deteccaodefalhas.dto.PythonDetectResponse;
import br.com.cabecadecone.deteccaodefalhas.entity.Analise;
import br.com.cabecadecone.deteccaodefalhas.repository.AnaliseRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class AnaliseService {

    private final AnaliseRepository repository;

    public AnaliseService(AnaliseRepository repository) {
        this.repository = repository;
    }

    public void salvar(PythonDetectResponse response) {
        Analise analise = new Analise();
        analise.setDataHora(LocalDateTime.now());
        analise.setHasFailure(response.has_failure());
        analise.setFailureType(response.failure_type());
        analise.setPredictedClass(response.predicted_class());
        analise.setConfidence(response.confidence());
        repository.save(analise);
    }

    public List<AnaliseResponse> listarTodas() {
        return repository.findAll().stream()
                .map(a -> new AnaliseResponse(
                        a.getId(),
                        a.getDataHora(),
                        a.getHasFailure(),
                        a.getFailureType(),
                        a.getPredictedClass(),
                        a.getConfidence()
                ))
                .toList();
    }
}
