import { ThemeToggle } from "@/components/ThemeToggle";
import { PromptSection } from "@/components/PromptSection";
export default function Home() {
  return (
    <div className="flex flex-col h-full p-2">
      <header className="flex items-center justify-end">
        <div className="p-2 pointer-cursor">
        <ThemeToggle/>

        </div>
      </header>
      <div className="flex-1">
        <PromptSection/>
      </div>
    </div>
  );
}
