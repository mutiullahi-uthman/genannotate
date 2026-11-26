"use client";

import {
  User,
  onAuthStateChanged,
  type Auth as FirebaseAuth,
} from "firebase/auth";

import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { useQueryClient } from "@tanstack/react-query";

import { getFirebaseAuth, isFirebaseConfigured } from "@/lib/firebase";
import {
  getCurrentUser,
  syncCurrentUser,
  type AccountProfile,
  type UserRole,
} from "@/services/auth";
import {
  createProject as createProjectRequest,
  getMyProjects,
  type Project,
  type ProjectMembership,
} from "@/services/projects";

type UserProfile = AccountProfile & { role: UserRole };
type AuthContextType = {
  user: User | null;
  profile: UserProfile | null;
  projects: ProjectMembership[];
  activeProject: ProjectMembership | null;
  loading: boolean;
  error: string | null;
  refreshProfile: () => void;
  selectProject: (projectId: string) => void;
  createProject: (name: string) => Promise<void>;
};

const AuthContext =
  createContext<AuthContextType>({
    user: null,
    profile: null,
    projects: [],
    activeProject: null,
    loading: true,
    error: null,
    refreshProfile: () => undefined,
    selectProject: () => undefined,
    createProject: async () => undefined,
  });

export function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [user, setUser] =
    useState<User | null>(null);

  const [profile, setProfile] =
    useState<UserProfile | null>(null);

  const [account, setAccount] = useState<AccountProfile | null>(null);
  const [projects, setProjects] = useState<ProjectMembership[]>([]);
  const [activeProject, setActiveProject] =
    useState<ProjectMembership | null>(null);

  const queryClient = useQueryClient();

  const [loading, setLoading] =
    useState(isFirebaseConfigured());

  const [profileError, setProfileError] =
    useState<string | null>(null);

  useEffect(() => {
    let firebaseAuth: FirebaseAuth;
    try {
      firebaseAuth = getFirebaseAuth();
    } catch {
      queueMicrotask(() => setLoading(false));
      return;
    }

    const unsubscribe = onAuthStateChanged(
      firebaseAuth,
      async (firebaseUser) => {
        setUser(firebaseUser);
        if (!firebaseUser) {
          setAccount(null);
          setProfile(null);
          setProjects([]);
          setActiveProject(null);
          setProfileError(null);
          setLoading(false);
          return;
        }

        setLoading(true);
        setProfileError(null);
        try {
          await syncCurrentUser();
          const [currentAccount, availableProjects] = await Promise.all([
            getCurrentUser(),
            getMyProjects(),
          ]);
          const savedProjectId =
            window.localStorage.getItem("active-project-id");
          const selectedProject =
            availableProjects.find(
              (project) => project.id === savedProjectId,
            ) ?? availableProjects[0] ?? null;

          setAccount(currentAccount);
          setProjects(availableProjects);
          setActiveProject(selectedProject);
          setProfile(
            selectedProject
              ? { ...currentAccount, role: selectedProject.role }
              : null,
          );
          if (selectedProject) {
            window.localStorage.setItem(
              "active-project-id",
              selectedProject.id,
            );
          } else {
            window.localStorage.removeItem("active-project-id");
          }
        } catch (error) {
          setAccount(null);
          setProfile(null);
          setProjects([]);
          setActiveProject(null);
          setProfileError(
            error instanceof Error
              ? error.message
              : "Your account profile could not be loaded.",
          );
        } finally {
          setLoading(false);
        }
      }
    );

    return () => unsubscribe();
  }, []);

  const refreshProfile = () => {
    if (user) {
      setLoading(true);
      setProfileError(null);
      void syncCurrentUser()
        .then(async () => {
          const [currentAccount, availableProjects] = await Promise.all([
            getCurrentUser(),
            getMyProjects(),
          ]);
          const selectedProject =
            availableProjects.find(
              (project) => project.id === activeProject?.id,
            ) ?? availableProjects[0] ?? null;
          setAccount(currentAccount);
          setProjects(availableProjects);
          setActiveProject(selectedProject);
          setProfile(
            selectedProject
              ? { ...currentAccount, role: selectedProject.role }
              : null,
          );
        })
        .catch((error: unknown) => {
          setAccount(null);
          setProfile(null);
          setProjects([]);
          setActiveProject(null);
          setProfileError(
            error instanceof Error
              ? error.message
              : "Your account profile could not be loaded.",
          );
        })
        .finally(() => setLoading(false));
    }
  };

  const selectProject = (projectId: string) => {
    const selectedProject = projects.find(
      (project) => project.id === projectId,
    );
    if (!selectedProject || !account) return;

    window.localStorage.setItem("active-project-id", projectId);
    setActiveProject(selectedProject);
    setProfile({ ...account, role: selectedProject.role });
    queryClient.clear();
  };

  const addProject = async (name: string) => {
    const created: Project = await createProjectRequest(name);
    const membership: ProjectMembership = {
      ...created,
      role: "ADMIN",
    };
    setProjects((current) => [...current, membership]);
    setActiveProject(membership);
    if (account) {
      setProfile({ ...account, role: membership.role });
    }
    window.localStorage.setItem("active-project-id", membership.id);
    queryClient.clear();
  };

  const error = profileError;

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        projects,
        activeProject,
        loading,
        error,
        refreshProfile,
        selectProject,
        createProject: addProject,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}