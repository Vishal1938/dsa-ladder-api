package dev.dsaladder.api;

import dev.dsaladder.api.Dtos.ExamDto;
import dev.dsaladder.api.Dtos.ProblemRow;
import dev.dsaladder.api.Dtos.StageDto;
import dev.dsaladder.api.Dtos.TopicDetail;
import dev.dsaladder.api.Dtos.TopicSummary;
import dev.dsaladder.problems.ProblemModel.Problem;
import dev.dsaladder.problems.ProblemModel.Topic;
import dev.dsaladder.problems.ProblemStore;
import dev.dsaladder.service.ProgressService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/topics")
public class TopicController {
    private final ProblemStore store;
    private final ProgressService progress;

    public TopicController(ProblemStore store, ProgressService progress) {
        this.store = store;
        this.progress = progress;
    }

    @GetMapping
    public List<TopicSummary> list() {
        ProgressService.Progress pr = progress.current();
        return store.topics().stream().map(t -> {
            List<Problem> ps = store.problems(t.id());
            int solved = (int) ps.stream().filter(p -> pr.solved().contains(p.slug())).count();
            return new TopicSummary(t.id(), t.name(), t.idea(), t.hasBook(), t.stages().size(), ps.size(), solved);
        }).toList();
    }

    @GetMapping("/{id}")
    public TopicDetail get(@PathVariable String id) {
        Topic t = store.topic(id);
        if (t == null) throw ApiException.notFound("Topic");
        ProgressService.Progress pr = progress.current();
        List<Problem> ps = store.problems(id);
        List<StageDto> stages = t.stages().stream().map(s -> new StageDto(s.index(), s.name(),
                ps.stream().filter(p -> p.stage() == s.index())
                        .map(p -> new ProblemRow(p.slug(), p.title(), p.difficulty(), p.whatsNew(), p.order(),
                                pr.solved().contains(p.slug()), pr.attempted().contains(p.slug())))
                        .toList(),
                s.exam().stream().map(e -> new ExamDto(e.id(), e.title(), e.url(), e.note(), e.rating())).toList())).toList();
        return new TopicDetail(t.id(), t.name(), t.idea(), t.triggers(), t.hasBook(), stages);
    }
}
