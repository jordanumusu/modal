import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "@/components/ui/sidebar"
import { SearchForm } from "@/components/SearchForm"
 
export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader>
      <SearchForm />
        </SidebarHeader>
      <SidebarContent>
        <SidebarGroup />
        <SidebarGroup />
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  )
}