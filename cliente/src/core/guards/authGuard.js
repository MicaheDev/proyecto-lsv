import axios from "axios";

export async function authGuard(to, from, next) {
  const userDataRaw = localStorage.getItem("user_data");
  const isAuthenticated = !!userDataRaw;

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin);

  if (requiresAuth && !isAuthenticated) {
    return next({ name: "Login" });
  }

  if (isAuthenticated && ["Login", "Register", "Home"].includes(to.name)) {
    return next({ name: "Learnning" });
  }

  if (requiresAdmin) {
    try {
      const parsedData = JSON.parse(userDataRaw);
      const response = await axios.get("http://127.0.0.1:5000/api/v1/verify", {
        headers: { Authorization: `Bearer ${parsedData?.token}` },
      });

      if (response.data.user.role_id !== 1) {
        return next({ name: "Learning" });
      }
    } catch {
      return next({ name: "Login" });
    }
  }

  next();
}
