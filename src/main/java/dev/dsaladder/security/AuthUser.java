package dev.dsaladder.security;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.Optional;

/** The authenticated principal stored in the security context. */
public record AuthUser(Long id, String email) {

    /** The signed-in user for the current request, if any. */
    public static Optional<AuthUser> current() {
        Authentication a = SecurityContextHolder.getContext().getAuthentication();
        return a != null && a.getPrincipal() instanceof AuthUser u ? Optional.of(u) : Optional.empty();
    }
}
