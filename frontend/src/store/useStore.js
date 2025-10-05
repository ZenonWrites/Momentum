import { create } from 'zustand';

const useStore = create((set) => ({
  token: null,
  user: null,
  profile: null,
  objectives: [],
  
  setToken: (token) => {
    global.authToken = token;
    set({ token });
  },
  
  setUser: (user) => set({ user }),
  
  setProfile: (profile) => set({ profile }),
  
  setObjectives: (objectives) => set({ objectives }),
  
  updateObjective: (id, updates) =>
    set((state) => ({
      objectives: state.objectives.map((obj) =>
        obj.id === id ? { ...obj, ...updates } : obj
      ),
    })),
  
  logout: () => {
    global.authToken = null;
    set({ token: null, user: null, profile: null, objectives: [] });
  },
}));

export default useStore;
