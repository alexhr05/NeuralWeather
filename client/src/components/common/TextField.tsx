import { useState, useId } from 'react'
import { twMerge } from 'tailwind-merge'

type TextFieldVariant = 'default' | 'underline'
type TextFieldSize = 'xs' | 'sm' | 'md' | 'lg'

type TextFieldProps = Omit<
  React.InputHTMLAttributes<HTMLInputElement>,
  "size"
> & {
  label?: string
  helperText?: string
  errorText?: string
  leadingIcon?: React.ReactNode
  trailingIcon?: React.ReactNode
  variant?: TextFieldVariant
  size?: TextFieldSize
  fullWidth?: boolean
  className?: string
  numeric?: boolean
  decimalPlaces?: number
  capitalze?: boolean
}

const variantStyles: Record<
  TextFieldVariant,
  { wrapper: string; input: string; focused: string; error: string }
> = {
  default: {
    wrapper:
      "bg-white/50 backdrop-blur-sm border border-zinc-200/80 rounded-xl hover:bg-white/70 hover:border-primary-tint-border transition-all duration-200",
    input: "bg-transparent",
    focused: "ring-0 bg-white/80 border-primary-ring",
    error: "border-error hover:border-error/90",
  },
  underline: {
    wrapper:
      "bg-transparent border-0 border-b-2 border-contrast/20 rounded-none hover:border-contrast/50 transition-colors duration-200",
    input: "bg-transparent",
    focused: "ring-0 border-contrast/80",
    error: "border-error hover:border-error/90",
  },
}

const sizeStyles: Record<
  TextFieldSize,
  { wrapper: string; input: string; icons: string; label: string }
> = {
  xs: {
    wrapper: "",
    input: "mx-2 my-0.5 text-xs",
    icons: "py-0.5 px-1.5",
    label: "text-[8px]",
  },
  sm: {
    wrapper: "",
    input: "mx-3 my-1.5 text-sm",
    icons: "p-1.5",
    label: "text-xs",
  },
  md: {
    wrapper: "",
    input: "mx-4 my-2.5 text-sm",
    icons: "p-2.5",
    label: "text-sm",
  },
  lg: {
    wrapper: "",
    input: "mx-4 my-3.5 text-base",
    icons: "p-3.5",
    label: "text-sm",
  },
}

export const TextField: React.FC<TextFieldProps> = ({
  label,
  helperText,
  errorText,
  leadingIcon,
  trailingIcon,
  variant = "default",
  size = "md",
  fullWidth = false,
  className = "",
  disabled = false,
  numeric = false,
  decimalPlaces = 2,
  capitalze = false,
  ...inputProps
}) => {
  const [focused, setFocused] = useState(false)
  const generatedId = useId()
  const id = inputProps.id ?? generatedId

  const hasError = Boolean(errorText)
  const v = variantStyles[variant]
  const s = sizeStyles[size]

  const wrapperClasses = [
    "flex items-center gap-2 overflow-hidden",
    v.wrapper,
    s.wrapper,
    focused ? v.focused : "",
    hasError ? v.error : "",
    disabled ? "opacity-50 cursor-not-allowed" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ")

  const inputClasses = [
    "flex-1 outline-none text-contrast placeholder-gray-400",
    s.input,
    v.input,
    disabled ? "cursor-not-allowed" : "",
    capitalze ? "capitalize" : "",
  ]
    .filter(Boolean)
    .join(" ")

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!numeric) {
      return inputProps.onKeyDown?.(e)
    }
    const allowed = [
      "Backspace",
      "Delete",
      "ArrowLeft",
      "ArrowRight",
      "Tab",
      "Enter",
      "Home",
      "End",
    ]
    if (allowed.includes(e.key)) {
      return
    }

    if (e.key === "-") {
      const { selectionStart, value } = e.currentTarget
      if (selectionStart === 0 && !value.includes("-")) {
        return
      }
      e.preventDefault()
      return
    }
    if (e.key === ".") {
      if (decimalPlaces > 0 && !e.currentTarget.value.includes(".")) {
        return
      }
      e.preventDefault()
      return
    }

    if (/[0-9]/.test(e.key)) {
      const { value, selectionStart, selectionEnd } = e.currentTarget
      const dotIndex = value.indexOf(".")
      if (
        decimalPlaces > 0 &&
        dotIndex !== -1 &&
        selectionStart !== null &&
        selectionEnd !== null &&
        selectionStart > dotIndex &&
        selectionStart === selectionEnd &&
        value.length - dotIndex - 1 >= decimalPlaces
      ) {
        e.preventDefault()
      }
      return
    }
    e.preventDefault()
    inputProps.onKeyDown?.(e)
  }

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    setFocused(false)
    inputProps.onBlur?.(e)
  }

  return (
    <div className={`flex flex-col gap-1 ${fullWidth ? "w-full" : "w-fit"}`}>
      {label && (
        <label
          htmlFor={id}
          className={`${s.label} font-medium ${
            hasError ? "text-error" : "text-contrast/70"
          }`}
        >
          {label}
        </label>
      )}

      <label htmlFor={id} className={wrapperClasses}>
        {leadingIcon && (
          <span
            className={twMerge(
              "text-contrast/80 shrink-0 bg-neutral/50",
              s.icons,
            )}
          >
            {leadingIcon}
          </span>
        )}
        <input
          id={id}
          disabled={disabled}
          className={inputClasses}
          onFocus={() => {
            setFocused(true)
          }}
          onBlur={handleBlur}
          onKeyDown={handleKeyDown}
          {...inputProps}
        />

        {trailingIcon && (
          <span
            className={twMerge(
              "text-contrast/80 shrink-0 bg-neutral/50 flex items-center self-stretch",
              s.icons,
            )}
          >
            {trailingIcon}
          </span>
        )}
      </label>

      {(helperText ?? errorText) && (
        <p
          className={`text-xs ${hasError ? "text-error" : "text-contrast/50"}`}
        >
          {errorText ?? helperText}
        </p>
      )}
    </div>
  )
}
