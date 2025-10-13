# ScriPTA Admin Panel - TypeScript Types

This directory contains comprehensive TypeScript type definitions for the ScriPTA Admin Panel, organized following TypeScript best practices.

## 📁 File Structure

```
src/types/
├── index.ts        # Main types and re-exports
├── api.ts          # API service types
├── components.ts   # React component types
└── README.md       # This file
```

## 📋 Type Categories

### 🎯 Domain Types (`index.ts`)

Core business domain types that represent the data structures used throughout the application:

- **Configuration Types**: `SwatchConfig`, `LayerConfig`, `TpmConfig`
- **Response Types**: `SwatchConfigResponse`, `LayerConfigResponse`, `TpmConfigResponse`
- **Enums**: `ColorModel`, `ColorSpace`, `LayerName`, `LayerColor`

### 🔌 API Types (`api.ts`)

Types specific to API communication and HTTP client functionality:

- **Service Interface**: `IApiService` - Contract for API service implementations
- **Request/Response**: `HttpRequestConfig`, `HttpResponse`
- **Error Handling**: `EnhancedApiError`, `ApiErrorType`
- **Advanced Features**: Caching, retries, interceptors, validation

### ⚛️ Component Types (`components.ts`)

React-specific types for component props, hooks, and UI interactions:

- **Base Props**: `BaseComponentProps` - Common props for all components
- **View Props**: `SwatchConfigViewProps`, `LayerConfigViewProps`, `TpmConfigViewProps`
- **Generic Components**: `TableProps`, `ModalProps`, `FormProps`
- **Hooks**: `UseDataResult`, `UseFilterResult`, `UsePaginationResult`

## 🏗️ TypeScript Best Practices Used

### 1. **Strict Type Safety**
```typescript
// Enums with const assertion for better tree-shaking
export const ApiErrorType = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  // ...
} as const;

export type ApiErrorType = typeof ApiErrorType[keyof typeof ApiErrorType];
```

### 2. **Generic Types for Reusability**
```typescript
export interface DataState<T> {
  data: T | null;
  loading: LoadingState;
  error: string | null;
}
```

### 3. **Utility Types for Flexibility**
```typescript
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

### 4. **Interface Segregation**
```typescript
// Separate concerns into focused interfaces
export interface LoadingProps { /* loading-specific */ }
export interface ErrorProps { /* error-specific */ }
export interface AsyncDataProps extends LoadingProps, ErrorProps {}
```

### 5. **Branded Types for Type Safety**
```typescript
// Example for future use
export type UserId = string & { readonly brand: unique symbol };
```

## 🎨 Usage Examples

### Importing Types

```typescript
// Import from main types module
import type { 
  SwatchConfig, 
  LayerConfigSet, 
  TpmConfig 
} from '../types';

// Import API-specific types
import type { 
  IApiService, 
  EnhancedApiError 
} from '../types/api';

// Import component-specific types
import type { 
  SwatchConfigViewProps, 
  TableProps 
} from '../types/components';
```

### Using Generic Types

```typescript
// Data fetching hook
const useConfigData = <T>(): UseDataResult<T> => {
  const [data, setData] = useState<T | null>(null);
  // ... implementation
  return { data, loading, error, refresh, isStale, lastUpdated };
};

// Usage
const swatchData = useConfigData<SwatchConfigResponse>();
const layerData = useConfigData<LayerConfigResponse>();
```

### Type-Safe API Service

```typescript
class ApiService implements IApiService {
  async getSwatchConfig(params?: GetSwatchConfigParams): Promise<{ swatches: SwatchConfig[] }> {
    // Implementation with full type safety
  }
}
```

### Component Props with Type Safety

```typescript
const SwatchConfigView: React.FC<SwatchConfigViewProps> = ({
  data,
  loading,
  error,
  onFilterChange,
  onRefresh,
  className,
  testId
}) => {
  // Fully typed component implementation
};
```

## 🔄 Future Enhancements

### CRUD Operations
Types are prepared for future CRUD functionality:

```typescript
// Form types are already defined
export interface FormProps<T> {
  values: T;
  onChange: (values: T) => void;
  onSubmit: (values: T) => void | Promise<void>;
  // ...
}

// Modal types for dialogs
export interface ModalProps {
  open: boolean;
  onClose: () => void;
  // ...
}
```

### Advanced API Features
- **Caching**: `CacheEntry<T>`, `CacheConfig`
- **Retries**: `RetryConfig`, `RetryState`
- **Interceptors**: `RequestInterceptor`, `ResponseInterceptor`
- **Validation**: `SchemaValidator<T>`, `ValidationResult<T>`

## 🛠️ Development Guidelines

### Adding New Types

1. **Identify the category**: Domain, API, or Component
2. **Place in appropriate file**: `index.ts`, `api.ts`, or `components.ts`
3. **Follow naming conventions**: 
   - Interfaces: `PascalCase`
   - Types: `PascalCase`
   - Enums: `PascalCase` (const objects with type assertion)

### Naming Conventions

- **Interfaces**: `SwatchConfig`, `ApiService`
- **Types**: `LoadingState`, `ApiErrorType`
- **Props**: `ComponentNameProps` (e.g., `SwatchConfigViewProps`)
- **Generics**: Single letter or descriptive (`T`, `TData`, `TConfig`)

### Export Strategy

- **Named exports**: Preferred for better tree-shaking
- **Type-only imports**: Use `import type` when importing only types
- **Re-exports**: Main `index.ts` re-exports from submodules

## 🧪 Testing Types

Types can be tested using TypeScript's type system:

```typescript
// Type assertion tests
type TestSwatchConfig = {
  colorName: string;
  colorModel: ColorModel;
  colorSpace: ColorSpace;
  colorValues: number[];
};

// Ensure SwatchConfig matches our expectations
const _typeTest: SwatchConfig = {} as TestSwatchConfig; // Should compile
```

## 📚 Additional Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)

This type system provides a solid foundation for type-safe development while maintaining flexibility for future enhancements and CRUD operations.