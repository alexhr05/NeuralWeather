import { type ComponentProps, useEffect, useRef, useState } from "react"
import { ChevronDown, ChevronUp, X } from "lucide-react"
import { TextField } from "./TextField"

type TextFieldProps = ComponentProps<typeof TextField>
type DropdownProps = TextFieldProps & {
  options: { label: string; value: string }[] | string[]
  placeholder?: string
  multiple?: boolean
  value: string | string[]
  onChange: (value: string | string[]) => void
}

export const Dropdown: React.FC<DropdownProps> = ({
  options,
  placeholder,
  value,
  onChange,
  multiple = false,
  ...textFieldProps
}) => {
  const [search, setSearch] = useState("")
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  const normalized = options.map(o =>
    typeof o === "string" ? { label: o, value: o } : o,
  )

  const selectedValues = multiple
    ? (value as string[])
    : value
      ? [value as string]
      : []

  const selectedOptions = normalized.filter(o =>
    selectedValues.includes(o.value),
  )

  const filtered = normalized.filter(o =>
    o.label.toLowerCase().includes(search.toLowerCase()),
  )

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener("mousedown", handler)
    return () => {
      document.removeEventListener("mousedown", handler)
    }
  }, [])

  const handleSelect = (optValue: string) => {
    if (multiple) {
      const current = value as string[]
      const next = current.includes(optValue)
        ? current.filter(v => v !== optValue)
        : [...current, optValue]
      onChange(next)
    } else {
      onChange(optValue)
      setOpen(false)
      setSearch("")
    }
  }

  const handleRemove = (optValue: string, e: React.MouseEvent) => {
    e.stopPropagation()
    const next = (value as string[]).filter(v => v !== optValue)
    onChange(next)
  }

  const displayValue = open
    ? search
    : multiple
      ? ""
      : (selectedOptions[0]?.label ?? "")

  return (
    <div
      ref={ref}
      className={`relative ${textFieldProps.fullWidth ? "w-full" : "w-fit"}`}
    >
      {multiple && selectedOptions.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-1.5">
          {selectedOptions.map(opt => (
            <span
              key={opt.value}
              className="flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-primary/10 text-primary border border-primary/20"
            >
              {opt.label}
              <X
                size={10}
                className="cursor-pointer hover:text-primary/60"
                onClick={e => {
                  handleRemove(opt.value, e)
                }}
              />
            </span>
          ))}
        </div>
      )}

      <TextField
        {...textFieldProps}
        value={displayValue}
        onFocus={() => {
          setOpen(true)
        }}
        onChange={e => {
          setSearch(e.target.value)
        }}
        placeholder={
          multiple && selectedOptions.length > 0 ? "Add more..." : placeholder
        }
        trailingIcon={
          <div
            onClick={e => {
              if (!textFieldProps.disabled) e.stopPropagation()
              e.preventDefault()
              setOpen(!open)
            }}
            className={textFieldProps.disabled ? "" : "cursor-pointer"}
          >
            {open ? <ChevronDown size={20} /> : <ChevronUp size={20} />}
          </div>
        }
      />

      {open && (
        <ul
          className="absolute z-50 mt-1 w-full max-h-30 overflow-scroll bg-neutral/90 backdrop-blur-lg rounded-xl shadow-xl"
          onMouseDown={e => e.preventDefault()}
        >
          {filtered.map(opt => {
            const isSelected = selectedValues.includes(opt.value)
            return (
              <li
                key={opt.value}
                className={`px-4 py-2.5 text-sm cursor-pointer transition-colors duration-150 flex items-center justify-between
                  ${textFieldProps.capitalze ? "capitalize" : ""}
                  ${isSelected ? "text-primary bg-primary/5" : "text-contrast hover:bg-neutral"}`}
                onClick={() => {
                  handleSelect(opt.value)
                }}
              >
                {opt.label}
                {multiple && isSelected && (
                  <div className="w-4 h-4 rounded-full bg-primary flex items-center justify-center shrink-0">
                    <X size={8} className="text-white" />
                  </div>
                )}
              </li>
            )
          })}
        </ul>
      )}
    </div>
  )
}
