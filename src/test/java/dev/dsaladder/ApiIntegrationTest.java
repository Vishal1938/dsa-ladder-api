package dev.dsaladder;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import dev.dsaladder.problems.ProblemStore;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class ApiIntegrationTest {
    @Autowired MockMvc mvc;
    @Autowired ObjectMapper json;
    @Autowired ProblemStore store;

    @Test
    void topicsAndProblemArePublic() throws Exception {
        mvc.perform(get("/api/topics")).andExpect(status().isOk()).andExpect(jsonPath("$[0].id").exists());
        mvc.perform(get("/api/topics/prefix-sum")).andExpect(status().isOk()).andExpect(jsonPath("$.stages[0].problems[0].slug").value("running-total"));
        mvc.perform(get("/api/problems/running-total")).andExpect(status().isOk()).andExpect(jsonPath("$.starterCode").exists());
        mvc.perform(get("/api/problems/nope")).andExpect(status().isNotFound());
    }

    @Test
    void registerSubmitAndSeeProgress() throws Exception {
        String body = json.writeValueAsString(Map.of("email", "ada@example.com", "password", "correct-horse", "displayName", "Ada"));
        String res = mvc.perform(post("/api/auth/register").contentType(MediaType.APPLICATION_JSON).content(body))
                .andExpect(status().isOk()).andReturn().getResponse().getContentAsString();
        String token = json.readTree(res).get("token").asText();

        String code = store.problem("running-total").referenceSolution();
        String verdict = mvc.perform(post("/api/problems/running-total/submit").header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("code", code))))
                .andExpect(status().isOk()).andReturn().getResponse().getContentAsString();
        JsonNode v = json.readTree(verdict);
        assertEquals("ACCEPTED", v.get("status").asText());
        assertTrue(v.get("saved").asBoolean());

        mvc.perform(get("/api/me/stats").header("Authorization", "Bearer " + token))
                .andExpect(status().isOk()).andExpect(jsonPath("$.solved").value(1));
        mvc.perform(get("/api/me/stats")).andExpect(status().isUnauthorized());
    }

    @Test
    void runWithCustomInput() throws Exception {
        String req = json.writeValueAsString(Map.of(
                "code", "class Solution { public long[] runningTotal(int[] nums) { return new long[nums.length]; } }",
                "inputs", java.util.List.of(java.util.List.of("[1,2]"))));
        mvc.perform(post("/api/problems/running-total/run").contentType(MediaType.APPLICATION_JSON).content(req))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("WRONG_ANSWER"))
                .andExpect(jsonPath("$.cases[0].expected").value("[1,3]"));
    }
}
