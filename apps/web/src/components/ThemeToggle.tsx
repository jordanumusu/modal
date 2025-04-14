"use client";

import { Moon, Sun } from "lucide-react";
import { Toggle } from "@/components/ui/toggle";
import { useEffect, useState } from "react";

export function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    setIsDark(document.documentElement.classList.contains("dark"));
  }, []);

  const toggleTheme = () => {
    document.documentElement.classList.toggle("dark");
    setIsDark(!isDark);
  };

  return (
    <Toggle
      onPressedChange={toggleTheme}
      aria-label="Toggle theme"
    >
      {isDark ? <Sun className="w-9 h-9" /> : <Moon className="w-9 h-9" />}
    </Toggle>
  );
}
