import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { TokenEditor, type TokenData } from './TokenEditor'

describe('TokenEditor', () => {
  const mockTokens: TokenData = {
    colors: {
      primary: { value: '#3B82F6', confidence: 0.92 },
      secondary: { value: '#10B981', confidence: 0.88 },
    },
    typography: {
      fontFamily: { value: 'Inter', confidence: 0.75 },
      fontSize: { value: '16px', confidence: 0.90 },
      fontWeight: { value: '500', confidence: 0.85 },
    },
    spacing: {
      padding: { value: '16px', confidence: 0.85 },
      margin: { value: '24px', confidence: 0.80 },
    },
  }

  describe('Rendering', () => {
    it('renders all token sections', () => {
      render(<TokenEditor tokens={mockTokens} />)
      
      expect(screen.getByTestId('token-editor')).toBeInTheDocument()
      expect(screen.getByText(/Colors \(2\)/)).toBeInTheDocument()
      expect(screen.getByText('Typography')).toBeInTheDocument()
      expect(screen.getByText(/Spacing \(2\)/)).toBeInTheDocument()
    })

    it('renders save and reset buttons', () => {
      render(<TokenEditor tokens={mockTokens} />)
      
      expect(screen.getByRole('button', { name: /reset/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /save changes/i })).toBeInTheDocument()
    })

    it('disables buttons initially (no changes)', () => {
      render(<TokenEditor tokens={mockTokens} />)
      
      const saveButton = screen.getByRole('button', { name: /save changes/i })
      const resetButton = screen.getByRole('button', { name: /reset/i })
      
      expect(saveButton).toBeDisabled()
      expect(resetButton).toBeDisabled()
    })
  })

  describe('Color Editing', () => {
    it('enables buttons when color changes', async () => {
      const user = userEvent.setup()
      render(<TokenEditor tokens={mockTokens} />)
      
      // Find and change primary color input
      const colorInputs = screen.getAllByRole('textbox')
      const primaryInput = colorInputs.find(input => 
        (input as HTMLInputElement).value === '#3B82F6'
      )
      
      expect(primaryInput).toBeDefined()
      
      if (primaryInput) {
        await user.clear(primaryInput)
        await user.type(primaryInput, '#FF5733')
        
        const saveButton = screen.getByRole('button', { name: /save changes/i })
        const resetButton = screen.getByRole('button', { name: /reset/i })
        
        expect(saveButton).toBeEnabled()
        expect(resetButton).toBeEnabled()
      }
    })
  })

  describe('Save Functionality', () => {
    it('calls onSave with edited tokens', async () => {
      const user = userEvent.setup()
      const onSave = vi.fn()
      
      render(<TokenEditor tokens={mockTokens} onSave={onSave} />)
      
      // Change a color
      const colorInputs = screen.getAllByRole('textbox')
      const primaryInput = colorInputs.find(input => 
        (input as HTMLInputElement).value === '#3B82F6'
      )
      
      if (primaryInput) {
        await user.clear(primaryInput)
        await user.type(primaryInput, '#FF5733')
        
        // Click save
        const saveButton = screen.getByRole('button', { name: /save changes/i })
        await user.click(saveButton)
        
        expect(onSave).toHaveBeenCalled()
        const savedTokens = onSave.mock.calls[0][0]
        expect(savedTokens.colors?.primary.value).toBe('#FF5733')
      }
    })

    it('disables buttons after save', async () => {
      const user = userEvent.setup()
      const onSave = vi.fn()
      
      render(<TokenEditor tokens={mockTokens} onSave={onSave} />)
      
      // Change a color
      const colorInputs = screen.getAllByRole('textbox')
      const primaryInput = colorInputs.find(input => 
        (input as HTMLInputElement).value === '#3B82F6'
      )
      
      if (primaryInput) {
        await user.clear(primaryInput)
        await user.type(primaryInput, '#FF5733')
        
        // Click save
        const saveButton = screen.getByRole('button', { name: /save changes/i })
        await user.click(saveButton)
        
        // Buttons should be disabled again
        expect(saveButton).toBeDisabled()
        expect(screen.getByRole('button', { name: /reset/i })).toBeDisabled()
      }
    })
  })

  describe('Reset Functionality', () => {
    it('reverts changes when reset clicked', async () => {
      const user = userEvent.setup()
      const onReset = vi.fn()
      
      render(<TokenEditor tokens={mockTokens} onReset={onReset} />)
      
      // Change a color
      const colorInputs = screen.getAllByRole('textbox')
      const primaryInput = colorInputs.find(input => 
        (input as HTMLInputElement).value === '#3B82F6'
      )
      
      if (primaryInput) {
        await user.clear(primaryInput)
        await user.type(primaryInput, '#FF5733')
        
        // Click reset
        const resetButton = screen.getByRole('button', { name: /reset/i })
        await user.click(resetButton)
        
        expect(onReset).toHaveBeenCalled()
        
        // Value should be back to original
        expect(screen.getByDisplayValue('#3B82F6')).toBeInTheDocument()
      }
    })
  })

  describe('Loading State', () => {
    it('disables buttons when loading', () => {
      render(<TokenEditor tokens={mockTokens} loading={true} />)
      
      expect(screen.getByRole('button', { name: /save changes/i })).toBeDisabled()
      expect(screen.getByRole('button', { name: /reset/i })).toBeDisabled()
    })

    it('shows loading text', () => {
      render(<TokenEditor tokens={mockTokens} loading={true} />)
      
      expect(screen.getByText('Saving...')).toBeInTheDocument()
    })
  })

  describe('Empty Sections', () => {
    it('does not render empty sections', () => {
      const emptyTokens: TokenData = {
        colors: {},
        typography: {},
        spacing: {},
      }
      
      render(<TokenEditor tokens={emptyTokens} />)
      
      expect(screen.queryByText(/Colors/)).not.toBeInTheDocument()
      expect(screen.queryByText(/Spacing/)).not.toBeInTheDocument()
    })

    it('renders typography section even when empty', () => {
      const tokensWithTypo: TokenData = {
        typography: {
          fontFamily: { value: 'Inter', confidence: 0.75 },
        },
      }
      
      render(<TokenEditor tokens={tokensWithTypo} />)
      
      expect(screen.getByText('Typography')).toBeInTheDocument()
    })
  })

  describe('Value Synchronization', () => {
    it('updates when external tokens change', () => {
      const { rerender } = render(<TokenEditor tokens={mockTokens} />)
      
      expect(screen.getByDisplayValue('#3B82F6')).toBeInTheDocument()
      
      const newTokens: TokenData = {
        colors: {
          primary: { value: '#FF5733', confidence: 0.92 },
        },
      }
      
      rerender(<TokenEditor tokens={newTokens} />)
      
      expect(screen.getByDisplayValue('#FF5733')).toBeInTheDocument()
    })
  })
})
