package dev.dsaladder.api;

import dev.dsaladder.security.AuthUser;
import dev.dsaladder.security.JwtService;
import dev.dsaladder.user.AppUser;
import dev.dsaladder.user.UserRepository;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    public record RegisterRequest(@Email @NotBlank @Size(max = 254) String email,
                                  @NotBlank @Size(min = 8, max = 72) String password,
                                  @NotBlank @Size(max = 60) String displayName) {}

    public record LoginRequest(@NotBlank String email, @NotBlank String password) {}

    public record UserDto(Long id, String email, String displayName) {
        static UserDto of(AppUser u) { return new UserDto(u.getId(), u.getEmail(), u.getDisplayName()); }
    }

    public record AuthResponse(String token, UserDto user) {}

    private final UserRepository users;
    private final PasswordEncoder encoder;
    private final JwtService jwt;

    public AuthController(UserRepository users, PasswordEncoder encoder, JwtService jwt) {
        this.users = users;
        this.encoder = encoder;
        this.jwt = jwt;
    }

    @PostMapping("/register")
    public AuthResponse register(@Valid @RequestBody RegisterRequest req) {
        String email = req.email().trim().toLowerCase();
        if (users.existsByEmailIgnoreCase(email)) throw new ApiException(HttpStatus.CONFLICT, "An account with this email already exists.");
        AppUser u = users.save(new AppUser(email, encoder.encode(req.password()), req.displayName().trim()));
        return new AuthResponse(jwt.issue(u), UserDto.of(u));
    }

    @PostMapping("/login")
    public AuthResponse login(@Valid @RequestBody LoginRequest req) {
        AppUser u = users.findByEmailIgnoreCase(req.email().trim())
                .filter(x -> encoder.matches(req.password(), x.getPasswordHash()))
                .orElseThrow(() -> new ApiException(HttpStatus.UNAUTHORIZED, "Wrong email or password."));
        return new AuthResponse(jwt.issue(u), UserDto.of(u));
    }

    @GetMapping("/me")
    public UserDto me() {
        AuthUser a = AuthUser.current().orElseThrow(() -> new ApiException(HttpStatus.UNAUTHORIZED, "Not signed in"));
        return users.findById(a.id()).map(UserDto::of).orElseThrow(() -> new ApiException(HttpStatus.UNAUTHORIZED, "Not signed in"));
    }
}
