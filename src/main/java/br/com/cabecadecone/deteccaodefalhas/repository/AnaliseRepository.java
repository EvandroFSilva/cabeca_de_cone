package br.com.cabecadecone.deteccaodefalhas.repository;

import br.com.cabecadecone.deteccaodefalhas.entity.Analise;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AnaliseRepository extends JpaRepository<Analise, Long> {
}
