import type { ReactNode } from "react"
import { twMerge } from "tailwind-merge"

type Variant = "primary" | "secondary" | "outline" | "ghost" | "glass"
type Size = "xs" | "sm" | "md" | "lg" | "icon"

export type ButtonProps = {
  variant?: Variant
  size?: Size
  disabled?: boolean
  children: ReactNode
  className?: string
  onClick?: () => void
  type?: "button" | "submit" | "reset"
}

const base =
  "relative inline-flex items-center justify-center font-semibold transition-all duration-200 active:scale-[0.97] cursor-pointer disabled:opacity-40 disabled:pointer-events-none select-none overflow-hidden"

const sizes: Record<Size, string> = {
  xs: "px-3 py-1 text-xs rounded-lg",
  sm: "px-4 py-1.5 text-xs rounded-xl",
  md: "px-6 py-2.5 text-sm rounded-xl",
  lg: "px-8 py-3.5 text-sm rounded-2xl tracking-wide",
  icon: "p-2 text-base rounded-full",
}

const variants: Record<Variant, string> = {
  primary:
    "bg-linear-to-br from-violet-500 to-purple-700 text-white shadow-lg shadow-violet-500/30 hover:shadow-violet-500/50 hover:brightness-110",
  secondary:
    "bg-zinc-100 text-zinc-800 hover:bg-zinc-200 shadow-sm",
  outline:
    "bg-transparent text-contrast border border-border hover:bg-zinc-50 shadow-sm",
  ghost:
    "bg-transparent text-muted hover:bg-zinc-100/80 hover:text-contrast",
  glass:
    "bg-violet-600/25 backdrop-blur-md text-violet-800 border border-violet-200/50 shadow-[0_4px_24px_rgba(139,92,246,0.15),inset_0_1px_1px_rgba(255,255,255,0.6)] hover:bg-violet-600/30 hover:shadow-[0_4px_32px_rgba(139,92,246,0.25),inset_0_1px_1px_rgba(255,255,255,0.7)] hover:bg-violet-800/30",
}

export const Button = ({
  variant = "primary",
  size = "md",
  disabled = false,
  children,
  className = "",
  onClick,
  type = "button",
  ...props
}: ButtonProps) => {
  return (
    <button
      className={twMerge(base, sizes[size], variants[variant], className)}
      disabled={disabled}
      onClick={onClick}
      type={type}
      {...props}
    >
      {/* Specular highlight — top sheen simulating light on glass */}
      {variant === "glass" && (
        <span className="pointer-events-none absolute inset-0 bg-linear-to-b from-white/40 to-transparent rounded-[inherit]" />
      )}
      <span className="relative z-10 inline-flex items-center">{children}</span>
    </button>
  )
}
