/// Minimal app user shape returned after successful sign-in.
class AppUser {
  final String id;
  final String email;
  final String displayName;
  final String? photoUrl;

  const AppUser({
    required this.id,
    required this.email,
    required this.displayName,
    this.photoUrl,
  });
}

/// Auth is abstracted so Phase 2 can swap the mock implementation for
/// FirebaseAuth (Google Sign-In + email/password) without touching any
/// widget code. Never call Firebase directly from presentation layer.
abstract class AuthRepository {
  Stream<AppUser?> authStateChanges();
  Future<AppUser> signInWithGoogle();
  Future<AppUser> signInWithEmail(String email, String password);
  Future<void> signOut();
}
