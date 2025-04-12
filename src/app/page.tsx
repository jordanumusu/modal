import { SidebarTrigger } from "@/components/ui/sidebar";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { PromptSection } from "@/components/PromptSection";
export default function Home() {
  return (
    <div className="flex flex-col h-full p-2">
      <header className="flex items-center justify-between">
        <SidebarTrigger className="" />
        <Avatar>
          <AvatarImage src="https://github.com/shadcn.png" />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
      </header>
      <div className="flex-1">
        <PromptSection/>
      </div>
    </div>
  );
}
