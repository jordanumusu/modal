import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { NewChatButton } from "@/components/NewChatButton";
import { Separator } from "@/components/ui/separator";
export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader >
        <div className="pt-2 w-full flex justify-around">
        <NewChatButton />
        </div>
        <Separator className="my-4" />

      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup />
        <SidebarGroup />
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
}
