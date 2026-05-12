import type { PathValue } from 'react-hook-form'
import {
  useFormContext,
  useWatch,
  type FieldPath,
  type FieldValues,
} from 'react-hook-form'
import { Dropdown } from '../common/Dropdown'
import type { ComponentProps } from 'react'

type DropdownProps = ComponentProps<typeof Dropdown>
type RHFDropdownProps<T extends FieldValues> = Omit<
  DropdownProps,
  "name" | "value" | "onChange"
> & {
  name: FieldPath<T>
}

export const RHFDropdown = <T extends FieldValues>({
  name,
  ...props
}: RHFDropdownProps<T>) => {
  const {
    setValue,
    formState: { errors },
  } = useFormContext<T>()

  const value = (useWatch({ name }) ?? "") as string

  const error = name.split(".").reduce<unknown>((acc, key) => {
    if (acc && typeof acc === "object" && key in acc) {
      return (acc as Record<string, unknown>)[key]
    }
    return undefined
  }, errors)

  const errorMessage =
    error && typeof error === "object" && "message" in error
      ? String((error as { message: unknown }).message)
      : undefined

  return (
    <Dropdown
      {...props}
      value={value}
      onChange={val => {
        setValue(name, val as PathValue<T, FieldPath<T>>)
      }}
      errorText={errorMessage}
    />
  )
}
