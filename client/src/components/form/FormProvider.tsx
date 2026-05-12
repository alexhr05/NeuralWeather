import { FormProvider as Form, type FieldValues, type UseFormReturn } from 'react-hook-form';

// ----------------------------------------------------------------------

type Props<T extends FieldValues> = {
  children: React.ReactNode;
  methods: UseFormReturn<T>;
  onSubmit: React.ComponentProps<"form">["onSubmit"];
  className?: string;
};

export default function FormProvider<T extends FieldValues>({ children, onSubmit, methods, className }: Props<T>) {
  return (
    <Form {...methods}>
      <form onSubmit={onSubmit} className={className}>{children}</form>
    </Form>
  );
}
