import {
  useFormContext,
  type FieldPath,
  type FieldValues,
} from "react-hook-form"

import { TextField } from "../common/TextField"
import type { ComponentProps } from "react"

type TextFieldProps = ComponentProps<typeof TextField>

type RHFTextFieldProps<T extends FieldValues> = Omit<TextFieldProps, "name"> & {
  name: FieldPath<T>
}

export const RHFTextField = <T extends FieldValues>({
  name,
  numeric,
  ...props
}: RHFTextFieldProps<T>) => {
  const {
    register,
    formState: { errors },
  } = useFormContext<T>()

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
    <TextField
      numeric={numeric}
      {...props}
      errorText={errorMessage}
      {...register(name, {
        setValueAs: (v: string) => {
          if (numeric) {
            return v === "" ? undefined : Number(v)
          }
          return v === "" ? undefined : v
        },
      })}
    />
  )
}
